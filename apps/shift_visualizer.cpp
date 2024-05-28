#include "ConfigManager.hpp"
#include "EventReader.hpp"
#include "ExtensionsHelpers.hpp"
#include "ShiftDetector.hpp"
#include "ShiftObjectsManager.hpp"
#include "ShiftVisualizationManager.hpp"

using namespace std;

void CheckArgs(int argc, char **argv) {
  if (argc != 2 && argc != 5) {
    fatal() << "Usage: " << argv[0] << " config_path" << endl;
    fatal() << "or" << endl;
    fatal() << argv[0] << " config_path input_path trees_output_path histograms_output_path" << endl;
    exit(1);
  }
}

int main(int argc, char **argv) {
  CheckArgs(argc, argv);
  info() << "config: " << argv[1] << endl;
  ConfigManager::Initialize(argv[1]);
  info() << " ConfigManager initialized" << endl;
  auto &config = ConfigManager::GetInstance();

  TApplication app("ROOT Application", &argc, argv);

  if (argc == 5) {
    config.SetInputPath(argv[2]);
    config.SetTreesOutputPath(argv[3]);
    config.SetHistogramsOutputPath(argv[4]);
  }

  auto eventReader = make_shared<EventReader>();
  auto shiftObjectsManager = make_unique<ShiftObjectsManager>();
  
  map<string, float> detectorParams;
  config.GetMap("detectorParams", detectorParams);

  string variant;
  config.GetValue("variant", variant);

  auto detector = make_shared<ShiftDetector>(detectorParams, variant == "lhcb");
  detector->Print();

  auto visuzalizationManager = make_shared<ShiftVisualizationManager>(detector, 2.0);
  set<shared_ptr<HepMCParticle>> visMuons;

  int startingEvent = 20;

  for (int iEvent = startingEvent; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);

    auto nMuons = make_shared<map<string, int>>();
    nMuons->insert({"1_hasMuons", 0});
    nMuons->insert({"2_triggerAndReco", 0});
    nMuons->insert({"3_intersectingDetector", 0});
    nMuons->insert({"4_beforeDetector", 0});
    nMuons->insert({"5_throughRock", 0});

    shiftObjectsManager->InsertIndexedParticles(event);
    shiftObjectsManager->InsertGoodZprimesCollection(event);
    shiftObjectsManager->InsertGoodDarkHadronsCollection(event);
    shiftObjectsManager->InsertGoodMuonsCollection(event);
    shiftObjectsManager->InsertMuonsHittingDetectorCollection(event, detectorParams, variant, nMuons);
    shiftObjectsManager->InsertGoodDarkPhotonsCollection(event);

    bool passes = true;
    for (auto &[key, value] : *nMuons) {
      if (value < 2) {
        passes = false;
        break;
      }
    }
    if (!passes) continue;

    // check that at least one combination of muons passes the mass cut
    bool passesMassCut = false;

    auto muons = event->GetCollection("muonsInDetector");
    for (int i = 0; i < muons->size(); i++) {
      auto physicsObject = muons->at(i);
      auto hepMCParticle = asHepMCParticle(physicsObject);
      auto fourVector = hepMCParticle->GetLorentzVector();

      visMuons.insert(hepMCParticle);

      for (int j = i + 1; j < muons->size(); j++) {
        auto physicsObject2 = muons->at(j);
        auto hepMCParticle2 = asHepMCParticle(physicsObject2);
        auto fourVector2 = hepMCParticle2->GetLorentzVector();

        visMuons.insert(hepMCParticle2);

        auto dimuon = fourVector + fourVector2;
        if (dimuon.M() > 11.0) {
          passesMassCut = true;
          break;
        }
      }
      if (passesMassCut) break;
    }
    if (!passesMassCut) continue;
    
    // if making visualization, break once the first passing event is found
    info() << "Passing event: " << iEvent << endl;
    break;
  }

  info() << "N muons: " << visMuons.size() << endl;

  visuzalizationManager->Visualize(visMuons);

  
  auto &logger = Logger::GetInstance();
  logger.Print();

  app.Run();
  return 0;
}