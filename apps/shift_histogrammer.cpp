#include "ConfigManager.hpp"
#include "EventReader.hpp"
#include "ExtensionsHelpers.hpp"
#include "HistogramsHandler.hpp"
#include "HistogramsFiller.hpp"
#include "ShiftObjectsManager.hpp"
#include "ShiftHistogramsFiller.hpp"

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

  if(argc == 4){
    auto &config = ConfigManager::GetInstance();
    config.SetInputPath(argv[2]);
    config.SetOutputPath(argv[3]);
  }

  auto eventReader = make_shared<EventReader>();

  auto histogramsHandler = make_shared<HistogramsHandler>();
  auto histogramsFiller = make_unique<HistogramsFiller>(histogramsHandler);
  auto shiftHistogramsFiller = make_unique<ShiftHistogramsFiller>(histogramsHandler);
  auto shiftObjectsManager = make_unique<ShiftObjectsManager>();
  
  // auto myHistogramsFiller = make_unique<MyHistogramsFiller>(histogramsHandler);
  
  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);

    shiftObjectsManager->InsertGoodZprimesCollection(event);
    shiftObjectsManager->InsertGoodDarkHadronsCollection(event);
    shiftObjectsManager->InsertGoodMuonsFromDarkHadronsCollection(event);
    
    histogramsFiller->FillDefaultVariables(event);
    shiftHistogramsFiller->Fill(event);
  }

  // Tell histogram handler to save histograms
  histogramsHandler->SaveHistograms();
  return 0;
}