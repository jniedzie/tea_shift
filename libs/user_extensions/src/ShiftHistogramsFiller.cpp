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

void ShiftHistogramsFiller::FillDarkPhotonHistograms(const shared_ptr<Event> event) {
  // Get the good Z' collection
  auto goodDarkPhotons = event->GetCollection("goodDarkPhotons");

  histogramsHandler->Fill("Event_nDarkPhotons", goodDarkPhotons->size(), GetWeight(event));

  // Loop over the good Dark Photon particles
  for (auto physicsObject : *goodDarkPhotons) {
    auto hepMCParticle = asHepMCParticle(physicsObject);
    auto fourVector = hepMCParticle->GetLorentzVector();

    histogramsHandler->Fill("DarkPhoton_mass", hepMCParticle->GetMass(), GetWeight(event));
    histogramsHandler->Fill("DarkPhoton_pt", fourVector.Pt(), GetWeight(event));
    histogramsHandler->Fill("DarkPhoton_eta", fourVector.Eta(), GetWeight(event));
    histogramsHandler->Fill("DarkPhoton_phi", fourVector.Phi(), GetWeight(event));
    histogramsHandler->Fill("DarkPhoton_pid", hepMCParticle->GetPid(), GetWeight(event));
    histogramsHandler->Fill("DarkPhoton_status", hepMCParticle->GetStatus(), GetWeight(event));
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

void ShiftHistogramsFiller::FillMuonHistograms(const shared_ptr<Event> event, string collectionName, string histName, double minEnergy) {
  auto muons = event->GetCollection(collectionName);

  histogramsHandler->Fill("Event_n" + histName, muons->size(), GetWeight(event));

  // Loop over the good muons from dark hadrons
  for (int i = 0; i < muons->size(); i++) {
    auto physicsObject = muons->at(i);

    float energy = physicsObject->Get("energy");
    if (energy < minEnergy) continue;

    auto hepMCParticle = asHepMCParticle(physicsObject);
    auto fourVector = hepMCParticle->GetLorentzVector();

    histogramsHandler->Fill(histName + "_mass", hepMCParticle->GetMass(), GetWeight(event));
    histogramsHandler->Fill(histName + "_pt", fourVector.Pt(), GetWeight(event));
    histogramsHandler->Fill(histName + "_energy", fourVector.E(), GetWeight(event));
    histogramsHandler->Fill(histName + "_eta", fourVector.Eta(), GetWeight(event));
    histogramsHandler->Fill(histName + "_phi", fourVector.Phi(), GetWeight(event));
    histogramsHandler->Fill(histName + "_pid", hepMCParticle->GetPid(), GetWeight(event));
    histogramsHandler->Fill(histName + "_status", hepMCParticle->GetStatus(), GetWeight(event));

    // mm -> m
    histogramsHandler->Fill(histName + "_x", hepMCParticle->GetX()/1000., GetWeight(event));
    histogramsHandler->Fill(histName + "_y", hepMCParticle->GetY()/1000., GetWeight(event));
    histogramsHandler->Fill(histName + "_z", hepMCParticle->GetZ()/1000., GetWeight(event));

    if (histName == "InitialMuons") {
      auto particles = event->GetCollection("Particle");
      auto mother = hepMCParticle->GetMother(particles);

      if (mother->GetPid() == 32 && fourVector.E() > 30) {
        histogramsHandler->Fill(histName + "FromDarkPhoton_eta", fourVector.Eta(), GetWeight(event));
        histogramsHandler->Fill(histName + "FromDarkPhoton_pt", fourVector.Pt(), GetWeight(event));
        histogramsHandler->Fill(histName + "FromDarkPhoton_energy", fourVector.E(), GetWeight(event));
      }
    }

    for (int j = i + 1; j < muons->size(); j++) {
      auto physicsObject2 = muons->at(j);
      auto hepMCParticle2 = asHepMCParticle(physicsObject2);
      auto fourVector2 = hepMCParticle2->GetLorentzVector();

      auto dimuon = fourVector + fourVector2;

      if (dimuon.M() < 11.0) continue;

      histogramsHandler->Fill(histName + "Pair_deltaR", fourVector.DeltaR(fourVector2), GetWeight(event));
      histogramsHandler->Fill(histName + "Pair_deltaEta", fourVector.Eta()-fourVector2.Eta(), GetWeight(event));
      histogramsHandler->Fill(histName + "Pair_deltaPhi", fabs(fourVector.DeltaPhi(fourVector2)), GetWeight(event));
      histogramsHandler->Fill(histName + "Pair_mass", dimuon.M(), GetWeight(event));
      histogramsHandler->Fill(histName + "Pair_lowMass", dimuon.M(), GetWeight(event));
    }
  }
}

void ShiftHistogramsFiller::Fill(const shared_ptr<Event> event, bool initial) {
  if (initial) {
    FillZprimeHistograms(event);
    FillDarkPhotonHistograms(event);
    FillDarkHadronsHistograms(event);
    FillMuonHistograms(event, "goodMuons", "InitialMuons");
    FillMuonHistograms(event, "goodMuons", "GoodInitialMuons", 30);
  } else {
    FillMuonHistograms(event, "muonsInDetector", "MuonsHittingDetector");
    auto muons = event->GetCollection("muonsInDetector");
    if (muons->size() >= 2) {
      histogramsHandler->Fill("Event_count", 0.5, GetWeight(event));
    }
  }
}
