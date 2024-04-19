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
  } catch (const Exception& e) {
    info() << "Weights branch not specified -- will assume weight is 1 for all events" << endl;
  }

  // Create an event processor
  eventProcessor = make_unique<EventProcessor>();
}

ShiftHistogramsFiller::~ShiftHistogramsFiller() {}

float ShiftHistogramsFiller::GetWeight(const std::shared_ptr<Event> event) {
  // Try to get event weight, otherwise set to 1.0
  float weight = 1.0;
  try {
    weight = event->Get(weightsBranchName);
  } catch (const Exception &e) {
  }
  return weight;
}

void ShiftHistogramsFiller::FillZprimeHistograms(const std::shared_ptr<Event> event) {
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

void ShiftHistogramsFiller::FillDarkHadronsHistograms(const std::shared_ptr<Event> event) {
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

void ShiftHistogramsFiller::Fill(const std::shared_ptr<Event> event) {
  FillZprimeHistograms(event);
  FillDarkHadronsHistograms(event);
}
