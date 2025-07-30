#include "ArgsManager.hpp"
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

int main(int argc, char **argv) {
  auto args = make_unique<ArgsManager>(argc, argv);

  if (!args->GetString("config").has_value()) {
    fatal() << "No config file provided" << endl;
    exit(1);
  }

  ConfigManager::Initialize(args->GetString("config").value());
  auto &config = ConfigManager::GetInstance();

  if (args->GetString("input_path").has_value()) {
    config.SetInputPath(args->GetString("input_path").value());
  }

  if (args->GetString("output_trees_path").has_value()) {
    config.SetTreesOutputPath(args->GetString("output_trees_path").value());
  }

  if (args->GetString("output_hists_path").has_value()) {
    config.SetHistogramsOutputPath(args->GetString("output_hists_path").value());
  }

  string inputFilePath;
  config.GetValue("inputFilePath", inputFilePath);
  info() << "Input file path: " << inputFilePath << endl;

  auto eventReader = make_shared<EventReader>();
  auto eventWriter = make_shared<EventWriter>(eventReader);
  auto histogramsHandler = make_shared<HistogramsHandler>();
  auto histogramsFiller = make_unique<HistogramsFiller>(histogramsHandler);
  auto shiftHistogramsFiller = make_unique<ShiftHistogramsFiller>(histogramsHandler);
  auto shiftObjectsManager = make_unique<ShiftObjectsManager>();
  auto cutFlowManager = make_shared<CutFlowManager>(eventReader, eventWriter);

  map<string, float> detectorParams;
  config.GetMap("detectorParams", detectorParams);

  string variant;
  config.GetValue("variant", variant);

  cutFlowManager->RegisterCut("initial");
  cutFlowManager->RegisterCut("hasNeutrinos");
  cutFlowManager->RegisterCut("intersectingDetector");
  cutFlowManager->RegisterCut("beforeDetector");

  auto detector = make_shared<ShiftDetector>(detectorParams, variant == "lhcb");
  detector->Print();

  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);

    cutFlowManager->UpdateCutFlow("initial");
    auto nNeutrinos = make_shared<map<string, int>>();
    nNeutrinos->insert({"1_hasNeutrinos", 0});
    nNeutrinos->insert({"2_intersectingDetector", 0});
    nNeutrinos->insert({"3_beforeDetector", 0});

    shiftObjectsManager->InsertIndexedParticles(event);
    shiftObjectsManager->InsertNeutrinosCollection(event);
    shiftObjectsManager->InsertNeutrinosHittingDetectorCollection(event, detectorParams, variant, nNeutrinos);

    shiftHistogramsFiller->Fill(event, true);

    bool passes = true;
    for (auto &[key, value] : *nNeutrinos) {
      if (value < 1) {
        passes = false;
        break;
      }
      // remove everything before underscore:
      string name = key.substr(key.find("_") + 1);
      cutFlowManager->UpdateCutFlow(name);
    }
    if (!passes) continue;

    shiftHistogramsFiller->Fill(event, false);

    auto neutrinosHittingDetector = event->GetCollection("neutrinosInDetector");
    vector<int> barcodesToKeep;
    for (auto neutrino : *neutrinosHittingDetector) {
      barcodesToKeep.push_back(neutrino->Get("barcode"));
    }

    auto particles = event->GetCollection("Particle");

    vector<int> keepIndices;

    for (int i = 0; i < particles->size(); ++i) {
      int barcode = particles->at(i)->Get("barcode");

      if (find(barcodesToKeep.begin(), barcodesToKeep.end(), barcode) != barcodesToKeep.end()) {
        keepIndices.push_back(i);
      }
    }

    eventWriter->AddCurrentHepMCevent("Events", keepIndices);
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