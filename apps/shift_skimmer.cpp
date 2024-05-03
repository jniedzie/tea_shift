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
    config.SetTreesOutputPath(argv[3]);
  }

  auto eventReader = make_shared<EventReader>();
  auto eventWriter = make_shared<EventWriter>(eventReader);
  auto cutFlowManager = make_shared<CutFlowManager>(eventReader, eventWriter);
  auto shiftObjectsManager = make_unique<ShiftObjectsManager>();
  auto hepMCProcessor = make_unique<HepMCProcessor>();

  map<string, float> detectorParams;
  config.GetMap("detectorParams", detectorParams);

  cutFlowManager->RegisterCut("initial");
  cutFlowManager->RegisterCut("hasMuons");
  cutFlowManager->RegisterCut("intersectingDetector");
  cutFlowManager->RegisterCut("beforeDetector");
  cutFlowManager->RegisterCut("throughRock");
  cutFlowManager->RegisterCut("triggerAndReco");
  
  auto detector = make_shared<ShiftDetector>(detectorParams);
  detector->Print();

  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);

    shiftObjectsManager->InsertGoodZprimesCollection(event);
    shiftObjectsManager->InsertGoodDarkHadronsCollection(event);
    shiftObjectsManager->InsertGoodMuonsCollection(event);

    cutFlowManager->UpdateCutFlow("initial");
    
    auto nMuons = make_shared<map<string, int>>();
    nMuons->insert({"1_hasMuons", 0});
    nMuons->insert({"2_intersectingDetector", 0});
    nMuons->insert({"3_beforeDetector", 0});
    nMuons->insert({"4_throughRock", 0});
    nMuons->insert({"5_triggerAndReco", 0});

    shiftObjectsManager->InsertMuonsHittingDetectorCollection(event, detectorParams, nMuons);

    bool passes = true;
    for(auto &[key, value] : *nMuons){
      if(value < 2){
        passes = false;
        break;
      }
      // remove everything before underscore:
      string name = key.substr(key.find("_") + 1);
      cutFlowManager->UpdateCutFlow(name);
    }
    if(!passes) continue;

    eventWriter->AddCurrentEvent("Events");
  }

  cutFlowManager->SaveCutFlow();
  cutFlowManager->Print();

  eventWriter->Save();

  auto &logger = Logger::GetInstance();
  logger.Print();

  return 0;
}