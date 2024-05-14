#include "ConfigManager.hpp"
#include "CutFlowManager.hpp"
#include "EventReader.hpp"
#include "ExtensionsHelpers.hpp"
#include "HistogramsFiller.hpp"
#include "HistogramsHandler.hpp"
#include "ShiftDetector.hpp"
#include "ShiftHistogramsFiller.hpp"
#include "ShiftObjectsManager.hpp"

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

  ConfigManager::Initialize(argv[1]);
  auto &config = ConfigManager::GetInstance();

  if (argc == 5) {
    config.SetInputPath(argv[2]);
    config.SetTreesOutputPath(argv[3]);
    config.SetHistogramsOutputPath(argv[4]);
  }

  auto eventReader = make_shared<EventReader>();
  auto eventWriter = make_shared<EventWriter>(eventReader);
  auto histogramsHandler = make_shared<HistogramsHandler>();
  auto histogramsFiller = make_unique<HistogramsFiller>(histogramsHandler);
  auto shiftHistogramsFiller = make_unique<ShiftHistogramsFiller>(histogramsHandler);
  auto shiftObjectsManager = make_unique<ShiftObjectsManager>();
  auto cutFlowManager = make_shared<CutFlowManager>(eventReader, eventWriter);

  map<string, float> detectorParams;
  config.GetMap("detectorParams", detectorParams);

  cutFlowManager->RegisterCut("initial");
  cutFlowManager->RegisterCut("hasMuons");
  cutFlowManager->RegisterCut("triggerAndReco");
  cutFlowManager->RegisterCut("intersectingDetector");
  cutFlowManager->RegisterCut("beforeDetector");
  cutFlowManager->RegisterCut("throughRock");
  cutFlowManager->RegisterCut("massCut");
  
  auto detector = make_shared<ShiftDetector>(detectorParams);
  detector->Print();

  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);

    cutFlowManager->UpdateCutFlow("initial");
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
    shiftObjectsManager->InsertMuonsHittingDetectorCollection(event, detectorParams, nMuons);
    shiftObjectsManager->InsertGoodDarkPhotonsCollection(event);

    shiftHistogramsFiller->Fill(event, true);

    bool passes = true;
    for (auto &[key, value] : *nMuons) {
      if (value < 2) {
        passes = false;
        break;
      }
      // remove everything before underscore:
      string name = key.substr(key.find("_") + 1);
      cutFlowManager->UpdateCutFlow(name);
    }
    if (!passes) continue;

    // check that at least one combination of muons passes the mass cut
    bool passesMassCut = false;

    auto muons = event->GetCollection("muonsInDetector");
    for (int i = 0; i < muons->size(); i++) {
      auto physicsObject = muons->at(i);
      auto hepMCParticle = asHepMCParticle(physicsObject);
      auto fourVector = hepMCParticle->GetLorentzVector();
      for (int j = i + 1; j < muons->size(); j++) {
        auto physicsObject2 = muons->at(j);
        auto hepMCParticle2 = asHepMCParticle(physicsObject2);
        auto fourVector2 = hepMCParticle2->GetLorentzVector();
        auto dimuon = fourVector + fourVector2;
        if(dimuon.M() > 11.0) {
          passesMassCut = true;
          break;
        }
      }
      if (passesMassCut) break;
    }
    if (!passesMassCut) continue;
    cutFlowManager->UpdateCutFlow("massCut");

    shiftHistogramsFiller->Fill(event, false);
    eventWriter->AddCurrentEvent("Events");
  }

  histogramsFiller->FillCutFlow(cutFlowManager);
  histogramsHandler->SaveHistograms();

  cutFlowManager->SaveCutFlow();
  cutFlowManager->Print();

  eventWriter->Save();

  auto &logger = Logger::GetInstance();
  logger.Print();

  return 0;
}