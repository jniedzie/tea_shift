#include "ConfigManager.hpp"
#include "CutFlowManager.hpp"
#include "EventReader.hpp"
#include "EventWriter.hpp"
#include "ExtensionsHelpers.hpp"
#include "HistogramsHandler.hpp"
#include "Profiler.hpp"
#include "HistogramsFiller.hpp"
#include "ShiftObjectsManager.hpp"
#include "HepMCProcessor.hpp"
#include "ShiftDetector.hpp"

using namespace std;

void CheckArgs(int argc, char **argv) {
  if (argc != 2 && argc != 4) {
    fatal() << "Usage: " << argv[0] << " config_path"<<endl;
    fatal() << "or"<<endl;
    fatal() << argv[0] << " config_path input_path output_path"<<endl;
    exit(1);
  }
}

int main(int argc, char **argv) {
  CheckArgs(argc, argv);
  
  ConfigManager::Initialize(argv[1]);
  auto &config = ConfigManager::GetInstance();

  if(argc == 4){    
    config.SetInputPath(argv[2]);
    config.SetOutputPath(argv[3]);
  }

  auto eventReader = make_shared<EventReader>();
  auto eventWriter = make_shared<EventWriter>(eventReader);
  auto cutFlowManager = make_shared<CutFlowManager>(eventReader, eventWriter);
  auto shiftObjectsManager = make_unique<ShiftObjectsManager>();
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

  auto detector = make_shared<ShiftDetector>(detectorParams);
  detector->Print();

  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);

    shiftObjectsManager->InsertGoodZprimesCollection(event);
    shiftObjectsManager->InsertGoodDarkHadronsCollection(event);
    shiftObjectsManager->InsertGoodMuonsFromDarkHadronsCollection(event);

    cutFlowManager->UpdateCutFlow("Initial");
    
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
      if(!detector->DoesParticleGoThrough(hepMCParticle)) continue;
      nMuonsIntersectingDetector++;

      // Check that the production vertex is before the detector
      if(!detector->IsProductionVertexBeforeTheEnd(hepMCParticle, 2.0)) continue;
      nMuonsBeforeDetector++;

      // Check that the muon goes through the rock
      if(!detector->DoesParticleGoThroughRock(hepMCParticle)) continue;
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

    eventWriter->AddCurrentEvent("Events");
  }

  cutFlowManager->SaveCutFlow();
  cutFlowManager->Print();

  eventWriter->Save();

  auto &logger = Logger::GetInstance();
  logger.Print();

  return 0;
}