#include "ConfigManager.hpp"
#include "CutFlowManager.hpp"
#include "EventReader.hpp"
#include "ExtensionsHelpers.hpp"
#include "HistogramsFiller.hpp"
#include "HistogramsHandler.hpp"
#include "ShiftHistogramsFiller.hpp"
#include "ShiftObjectsManager.hpp"
#include "HepMCProcessor.hpp"
#include "ShiftDetector.hpp"

using namespace std;

void CheckArgs(int argc, char **argv) {
  if (argc != 2 && argc != 4) {
    fatal() << "Usage: " << argv[0] << " config_path" << endl;
    fatal() << "or" << endl;
    fatal() << argv[0] << " config_path input_path output_path" << endl;
    exit(1);
  }
}

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
  auto cutFlowManager = make_shared<CutFlowManager>(eventReader);
  
  map<string, float> detectorParams;
  config.GetMap("detectorParams", detectorParams);

  cutFlowManager->RegisterCut("initial");

  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);

    cutFlowManager->UpdateCutFlow("initial");

    shiftObjectsManager->InsertGoodZprimesCollection(event);
    shiftObjectsManager->InsertGoodDarkHadronsCollection(event);
    shiftObjectsManager->InsertGoodMuonsCollection(event);
    shiftObjectsManager->InsertMuonsHittingDetectorCollection(event, detectorParams);
    shiftHistogramsFiller->Fill(event);
  }

  histogramsFiller->FillCutFlow(cutFlowManager);

  histogramsHandler->SaveHistograms();
  cutFlowManager->Print();

  auto &logger = Logger::GetInstance();
  logger.Print();

  return 0;
}