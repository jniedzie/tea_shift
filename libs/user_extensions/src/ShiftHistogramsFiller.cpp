#include "ShiftHistogramsFiller.hpp"

#include "ConfigManager.hpp"
#include "ExtensionsHelpers.hpp"

using namespace std;

ShiftHistogramsFiller::ShiftHistogramsFiller(shared_ptr<HistogramsHandler> histogramsHandler_) : histogramsHandler(histogramsHandler_) {
  // Create a config manager
  auto &config = ConfigManager::GetInstance();

  // Try to read weights branch
  try {
    config.GetValue("weightsBranchName", weightsBranchName);
  } catch (const Exception &e) {
    info() << "Weights branch not specified -- will assume weight is 1 for all events" << endl;
  }

  // Create an event processor
  eventProcessor = make_unique<EventProcessor>();
}

ShiftHistogramsFiller::~ShiftHistogramsFiller() {}

float ShiftHistogramsFiller::GetWeight(const shared_ptr<Event> event) {
  // Try to get event weight, otherwise set to 1.0
  float weight = 1.0;
  try {
    weight = event->Get(weightsBranchName);
  } catch (const Exception &e) {
  }
  return weight;
}

void ShiftHistogramsFiller::FillZprimeHistograms(const shared_ptr<Event> event) {
  // Get the good Z' collection
  auto goodZprimes = event->GetCollection("goodZprimes");

  histogramsHandler->Fill("Event_nZprimes", goodZprimes->size(), GetWeight(event));

  // Loop over the good Z' particles
  for (auto physicsObject : *goodZprimes) {
    auto hepMCParticle = asHepMCParticle(physicsObject);
    auto fourVector = hepMCParticle->GetLorentzVector();

    histogramsHandler->Fill("Zprime_mass", hepMCParticle->GetMass(), GetWeight(event));
    histogramsHandler->Fill("Zprime_pt", fourVector.Pt(), GetWeight(event));
    histogramsHandler->Fill("Zprime_eta", fourVector.Eta(), GetWeight(event));
    histogramsHandler->Fill("Zprime_phi", fourVector.Phi(), GetWeight(event));
    histogramsHandler->Fill("Zprime_pid", hepMCParticle->GetPid(), GetWeight(event));
    histogramsHandler->Fill("Zprime_status", hepMCParticle->GetStatus(), GetWeight(event));
  }
}

void ShiftHistogramsFiller::FillDarkHadronsHistograms(const shared_ptr<Event> event) {
  // Get the good dark hadrons collection
  auto goodDarkHadrons = event->GetCollection("goodDarkHadrons");

  histogramsHandler->Fill("Event_nDarkHadrons", goodDarkHadrons->size(), GetWeight(event));

  // Loop over the good dark hadrons
  for (auto physicsObject : *goodDarkHadrons) {
    auto hepMCParticle = asHepMCParticle(physicsObject);
    auto fourVector = hepMCParticle->GetLorentzVector();

    histogramsHandler->Fill("DarkHadron_mass", hepMCParticle->GetMass(), GetWeight(event));
    histogramsHandler->Fill("DarkHadron_pt", fourVector.Pt(), GetWeight(event));
    histogramsHandler->Fill("DarkHadron_eta", fourVector.Eta(), GetWeight(event));
    histogramsHandler->Fill("DarkHadron_phi", fourVector.Phi(), GetWeight(event));
    histogramsHandler->Fill("DarkHadron_pid", hepMCParticle->GetPid(), GetWeight(event));
    histogramsHandler->Fill("DarkHadron_status", hepMCParticle->GetStatus(), GetWeight(event));
  }
}

void ShiftHistogramsFiller::FillMuonHistograms(const shared_ptr<Event> event, string collectionName, string histName) {
  auto muons = event->GetCollection(collectionName);

  histogramsHandler->Fill("Event_n"+histName, muons->size(), GetWeight(event));

  // Loop over the good muons from dark hadrons
  for (int i = 0; i < muons->size(); i++) {
    auto physicsObject = muons->at(i);
    auto hepMCParticle = asHepMCParticle(physicsObject);
    auto fourVector = hepMCParticle->GetLorentzVector();

    histogramsHandler->Fill(histName+"_mass", hepMCParticle->GetMass(), GetWeight(event));
    histogramsHandler->Fill(histName+"_pt", fourVector.Pt(), GetWeight(event));
    histogramsHandler->Fill(histName+"_energy", fourVector.E(), GetWeight(event));
    histogramsHandler->Fill(histName+"_eta", fourVector.Eta(), GetWeight(event));
    histogramsHandler->Fill(histName+"_phi", fourVector.Phi(), GetWeight(event));
    histogramsHandler->Fill(histName+"_pid", hepMCParticle->GetPid(), GetWeight(event));
    histogramsHandler->Fill(histName+"_status", hepMCParticle->GetStatus(), GetWeight(event));

    histogramsHandler->Fill(histName+"_x", hepMCParticle->GetX(), GetWeight(event));
    histogramsHandler->Fill(histName+"_y", hepMCParticle->GetY(), GetWeight(event));
    histogramsHandler->Fill(histName+"_z", hepMCParticle->GetZ(), GetWeight(event));
    for (int j = i + 1; j < muons->size(); j++) {
      auto physicsObject2 = muons->at(j);
      auto hepMCParticle2 = asHepMCParticle(physicsObject2);
      auto fourVector2 = hepMCParticle2->GetLorentzVector();

      auto dimuon = fourVector + fourVector2;

      histogramsHandler->Fill(histName+"Pair_deltaR", fourVector.DeltaR(fourVector2), GetWeight(event));
      histogramsHandler->Fill(histName+"Pair_mass", dimuon.M(), GetWeight(event));
      histogramsHandler->Fill(histName+"Pair_lowMass", dimuon.M(), GetWeight(event));
    }
  }
}

void ShiftHistogramsFiller::Fill(const shared_ptr<Event> event) {
  FillZprimeHistograms(event);
  FillDarkHadronsHistograms(event);

  FillMuonHistograms(event, "goodMuons", "InitialMuons");
  FillMuonHistograms(event, "muonsInDetector", "MuonsHittingDetector");

  auto muons = event->GetCollection("muonsInDetector");
  if(muons->size() >= 2){
    histogramsHandler->Fill("Event_count", 0.5, GetWeight(event));
  }
}
