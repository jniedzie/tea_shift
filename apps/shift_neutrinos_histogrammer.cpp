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

int main(int argc, char** argv) {
  vector<string> requiredArgs = {"config"};
  vector<string> optionalArgs = {"input_path", "output_hists_path", "output_trees_path"};
  auto args = make_unique<ArgsManager>(argc, argv, requiredArgs, optionalArgs);
  ConfigManager::Initialize(args);

  auto& config = ConfigManager::GetInstance();
  string inputFilePath;
  config.GetValue("inputFilePath", inputFilePath);
  info() << "Input file path: " << inputFilePath << endl;

  auto eventReader = make_shared<EventReader>();
  auto eventWriter = make_shared<EventWriter>(eventReader);
  auto histogramsHandler = make_shared<HistogramsHandler>();
  auto histogramsFiller = make_unique<HistogramsFiller>(histogramsHandler);
  auto shiftHistogramsFiller = make_unique<ShiftHistogramsFiller>(histogramsHandler);

  auto cutFlowManager = make_shared<CutFlowManager>(eventReader, eventWriter);

  map<string, float> detectorParams;
  config.GetMap("detectorParams", detectorParams);

  string variant;
  config.GetValue("variant", variant);

  auto shiftObjectsManager = make_unique<ShiftObjectsManager>(detectorParams, variant);

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
    shiftObjectsManager->InsertNeutrinosHittingDetectorCollection(event, nNeutrinos);

    shiftHistogramsFiller->Fill(event, true);

    bool passes = true;
    for (auto& [key, value] : *nNeutrinos) {
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

  // auto hist = histogramsHandler->GetHistogram1D({"NeutrinosHittingDetector_phi", ""});
  // hist->Rebin(3);
  // hist->SaveAs("../hist.root");

  // double mean = 0;
  // int nNonZeroBins = 0;

  // // First, compute the average bin content (excluding underflow/overflow)
  // for (int i = 1; i <= hist->GetNbinsX(); ++i) {
  //   if (hist->GetBinContent(i) <= 0) continue; // skip bins with zero content
  //   if(fabs(hist->GetBinCenter(i)) > 2.9) continue; // skip bins outside the range of interest
  //   mean += hist->GetBinContent(i);
  //   ++nNonZeroBins;
  // }
  // mean /= nNonZeroBins;

  // // Now compute chi2
  // double chi2_flat = 0;
  // for (int i = 1; i <= hist->GetNbinsX(); ++i) {
  //   if (hist->GetBinContent(i) <= 0) continue; // skip bins with zero content
  //   if(fabs(hist->GetBinCenter(i)) > 2.9) continue; // skip bins outside the range of interest
  //   double content = hist->GetBinContent(i);
  //   double error = hist->GetBinError(i);

  //   // skip bins with zero error to avoid division by zero
  //   if (error <= 0) continue;

  //   double delta = content - mean;
  //   chi2_flat += (delta * delta) / (error * error);
  // }

  // double chi2_per_ndf = chi2_flat / nNonZeroBins;

  // std::cout << "Flatness chi2/NDF: " << chi2_per_ndf << std::endl;

  // double valueAtZero = hist->GetBinContent(hist->FindFixBin(0.0));
  // double valueAtThree = hist->GetBinContent(hist->FindFixBin(2.9));
  // double sigma = hist->GetBinError(hist->FindBin(0.0));
  // double distanceInSigmas = (valueAtZero - valueAtThree) / sigma;
  // info() << "Distance in sigmas between value at 0.0 and value at 3.0: " << distanceInSigmas << endl;
  // info() << "Value at 0.0: " << valueAtZero << ", Value at 3.0: " << valueAtThree << endl;

  histogramsHandler->SaveHistograms();

  cutFlowManager->SaveCutFlow();
  cutFlowManager->Print();

  eventWriter->Save();

  auto& logger = Logger::GetInstance();
  logger.Print();

  return 0;
}