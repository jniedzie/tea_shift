#include "ConfigManager.hpp"
#include "CutFlowManager.hpp"
#include "EventReader.hpp"
#include "ExtensionsHelpers.hpp"
#include "HistogramsFiller.hpp"
#include "HistogramsHandler.hpp"
#include "ShiftHistogramsFiller.hpp"
#include "ShiftObjectsManager.hpp"
#include "HepMCProcessor.hpp"

using namespace std;

void CheckArgs(int argc, char **argv) {
  if (argc != 2 && argc != 4) {
    fatal() << "Usage: " << argv[0] << " config_path" << endl;
    fatal() << "or" << endl;
    fatal() << argv[0] << " config_path input_path output_path" << endl;
    exit(1);
  }
}

class ShiftDetector {
  // Class to describe a spherical detector located at (x,y,z) coordinates with a given radius
 public:
  ShiftDetector(float _x, float _y, float _z, float _radius) : x(_x), y(_y), z(_z), radius(_radius) {}
  ~ShiftDetector() {}

  bool DoesParticleGoThrough(const shared_ptr<HepMCParticle> &particle){
    // check if the particle, given it's eta and phi, as well as production vertex x,y,z, passes through this sphere (ignore the magnetic field)
    auto fourVector = particle->GetLorentzVector();
    float eta = fourVector.Eta();
    float theta = 2 * atan(exp(-eta));
    float phi = fourVector.Phi();
    float xProd = particle->GetX() / 1e3; // convert mm to m
    float yProd = particle->GetY() / 1e3; // convert mm to m
    float zProd = particle->GetZ() / 1e3; // convert mm to m

    // Direction vector components
    double dx = cos(phi) * sin(theta);
    double dy = sin(phi) * sin(theta);
    double dz = cos(theta);

    // Calculate coefficients of the quadratic equation
    double a = dx * dx + dy * dy + dz * dz;
    double b = 2 * (dx * (xProd - x) + dy * (yProd - y) + dz * (zProd - z));
    double c = (xProd - x) * (xProd - x)
             + (yProd - y) * (yProd - y)
             + (zProd - z) * (zProd - z)
             - radius * radius;

    // Calculate the discriminant
    double discriminant = b * b - 4 * a * c;

    // Check if the discriminant is non-negative
    return discriminant >= 0;
  }

  bool IsProductionVertexBeforeTheEnd(const shared_ptr<HepMCParticle> &particle, float maxDistanceInsideDetector=0.0){
    // check if the production vertex of the particle is before the detector, or at most 1m past the detector's center
    float xProd = particle->GetX() / 1e3; // convert mm to m
    float yProd = particle->GetY() / 1e3; // convert mm to m
    float zProd = particle->GetZ() / 1e3; // convert mm to m

    float particleDistance = sqrt(pow(xProd, 2)+pow(yProd, 2)+pow(zProd, 2));
    float detectorDistance = sqrt(pow(x, 2)+pow(y, 2)+pow(z, 2));
    return particleDistance < detectorDistance + maxDistanceInsideDetector;
  }

  bool DoesParticleGoThroughRock(const shared_ptr<HepMCParticle> &particle){
    // calculate the distance the particle has to travel from production vertex to the edge of the detector
    float xProd = particle->GetX() / 1e3; // convert mm to m
    float yProd = particle->GetY() / 1e3; // convert mm to m
    float zProd = particle->GetZ() / 1e3; // convert mm to m

    float particleDistance = sqrt(pow(xProd, 2)+pow(yProd, 2)+pow(zProd, 2));
    float detectorDistance = sqrt(pow(x, 2)+pow(y, 2)+pow(z, 2));
    float distanceToDetector = detectorDistance - particleDistance - radius;

    float particleEnergy = particle->GetLorentzVector().E();

    return particleEnergy > distanceToDetector;
  }

 private:
  float x, y, z, radius; // Coordinates of the detector and its radius (m)
};

int main(int argc, char **argv) {
  CheckArgs(argc, argv);

  ConfigManager::Initialize(argv[1]);
  auto &config = ConfigManager::GetInstance();

  if (argc == 4) {
    
    config.SetInputPath(argv[2]);
    config.SetOutputPath(argv[3]);
  }

  auto eventReader = make_shared<EventReader>();

  auto histogramsHandler = make_shared<HistogramsHandler>();
  auto histogramsFiller = make_unique<HistogramsFiller>(histogramsHandler);
  auto shiftHistogramsFiller = make_unique<ShiftHistogramsFiller>(histogramsHandler);
  auto shiftObjectsManager = make_unique<ShiftObjectsManager>();
  auto cutFlowManager = make_unique<CutFlowManager>(eventReader);
  auto hepMCProcessor = make_unique<HepMCProcessor>();

  map<string, float> detectorParams;
  config.GetMap("detectorParams", detectorParams);

  cutFlowManager->RegisterCut("Initial");
  cutFlowManager->RegisterCut("atLeastTwoMuons");
  cutFlowManager->RegisterCut("muonInCMS");
  cutFlowManager->RegisterCut("muonBeforeCMS");
  cutFlowManager->RegisterCut("passesThroughRock");
  cutFlowManager->RegisterCut("triggerAndReco");
  cutFlowManager->RegisterCut("goodDimuons");

  auto cmsDetector = make_shared<ShiftDetector>(detectorParams["x"], detectorParams["y"], detectorParams["z"], detectorParams["radius"]);

  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);

    shiftObjectsManager->InsertGoodZprimesCollection(event);
    shiftObjectsManager->InsertGoodDarkHadronsCollection(event);
    shiftObjectsManager->InsertGoodMuonsFromDarkHadronsCollection(event);

    cutFlowManager->UpdateCutFlow("Initial");
    shiftHistogramsFiller->Fill(event);

    auto goodMuonsFromDarkHadrons = event->GetCollection("goodMuonsFromDarkHadrons");

    int nMuonsFromDarkHadrons = 0;
    int nMuonsIntersectingDetector = 0;
    int nMuonsBeforeDetector = 0;
    int nMuonsThroughRock = 0;
    int nMuonsTriggerAndReco = 0;

    vector<shared_ptr<HepMCParticle>> passingMuons;

    for (auto physicsObject : *goodMuonsFromDarkHadrons) {
      auto hepMCParticle = asHepMCParticle(physicsObject);
      
      // Count muons from dark hadrons
      nMuonsFromDarkHadrons++;

      // Check that they intersect with the detector
      if(!cmsDetector->DoesParticleGoThrough(hepMCParticle)) continue;
      nMuonsIntersectingDetector++;

      // Check that the production vertex is before the detector
      if(!cmsDetector->IsProductionVertexBeforeTheEnd(hepMCParticle, 2.0)) continue;
      nMuonsBeforeDetector++;

      // Check that the muon goes through the rock
      if(!cmsDetector->DoesParticleGoThroughRock(hepMCParticle)) continue;
      nMuonsThroughRock++;

      // Check that the muon has at least 30 GeV of energy, so that it can trigger and be reconstructed at CMS
      if(hepMCParticle->GetLorentzVector().E() < 30) continue;
      nMuonsTriggerAndReco++;


      passingMuons.push_back(hepMCParticle);
    }

    if (nMuonsFromDarkHadrons < 2) continue;
    cutFlowManager->UpdateCutFlow("atLeastTwoMuons");

    if(nMuonsIntersectingDetector < 2) continue;
    cutFlowManager->UpdateCutFlow("muonInCMS");

    if(nMuonsBeforeDetector < 2) continue;
    cutFlowManager->UpdateCutFlow("muonBeforeCMS");

    if(nMuonsThroughRock < 2) continue;
    cutFlowManager->UpdateCutFlow("passesThroughRock");

    if(nMuonsTriggerAndReco < 2) continue;
    cutFlowManager->UpdateCutFlow("triggerAndReco");


    vector<pair<shared_ptr<HepMCParticle>, shared_ptr<HepMCParticle>>> dimuons;

    auto allParticles = event->GetCollection("Particle");

    for(int i=0; i<passingMuons.size(); i++){
      for(int j=i+1; j<passingMuons.size(); j++){
        auto muon1 = passingMuons[i];
        auto muon2 = passingMuons[j];

        auto commonMother = hepMCProcessor->GetCommonMother(muon1, muon2, allParticles);
        if(!commonMother) continue;

        dimuons.push_back({muon1, muon2});
      }
    }

    if(dimuons.size() == 0) continue;
    cutFlowManager->UpdateCutFlow("goodDimuons");


  }

  // Tell histogram handler to save histograms
  histogramsHandler->SaveHistograms();

  cutFlowManager->Print();
  return 0;
}