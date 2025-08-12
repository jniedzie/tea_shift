#include "ShiftObjectsManager.hpp"

#include "ConfigManager.hpp"
#include "Logger.hpp"
#include "Profiler.hpp"

using namespace std;

ShiftObjectsManager::ShiftObjectsManager(const map<string, float> &detectorParams, string variant) {
  auto &config = ConfigManager::GetInstance();

  hepMCProcessor = make_unique<HepMCProcessor>();
  detector = make_unique<ShiftDetector>(detectorParams, variant == "lhcb");
}

void ShiftObjectsManager::InsertIndexedParticles(shared_ptr<Event> event) {
  auto particles = event->GetCollection("Particle");
  auto indexedParticles = make_shared<PhysicsObjects>();

  for (int particleIndex = 0; particleIndex < particles->size(); particleIndex++) {
    auto physicsObject = particles->at(particleIndex);
    physicsObject->SetIndex(particleIndex);
    indexedParticles->push_back(physicsObject);
  }
  event->AddCollection("IndexedParticles", indexedParticles);
}

bool ShiftObjectsManager::IsGoodZprime(const shared_ptr<HepMCParticle> particle, const shared_ptr<PhysicsObjects> &allParticles) {
  if (particle->GetPid() != 4900023) return false;
  if (!hepMCProcessor->IsLastCopy(particle, allParticles)) return false;
  return true;
}

bool ShiftObjectsManager::IsGoodDarkPhoton(const shared_ptr<HepMCParticle> particle, const shared_ptr<PhysicsObjects> &allParticles) {
  if (particle->GetPid() != 32) return false;
  if (!hepMCProcessor->IsLastCopy(particle, allParticles)) return false;
  return true;
}

bool ShiftObjectsManager::IsGoodDarkHadron(const shared_ptr<HepMCParticle> particle, const shared_ptr<PhysicsObjects> &allParticles) {
  if (fabs(particle->GetPid()) != 4900111 && fabs(particle->GetPid()) != 4900113) return false;
  if (!hepMCProcessor->IsLastCopy(particle, allParticles)) return false;
  return true;
}

bool ShiftObjectsManager::IsGoodMuon(const shared_ptr<HepMCParticle> particle, const shared_ptr<PhysicsObjects> &allParticles) {
  if (fabs(particle->GetPid()) != 13) return false;
  if (!hepMCProcessor->IsLastCopy(particle, allParticles)) return false;

  // auto mother = particle->GetMother(allParticles);

  // if(mother->GetPid() != 4900111 && mother->GetPid() != 4900113) {
  //   info() << "Mother pid: " << mother->GetPid() << endl;
  //   return false;
  // }
  return true;
}

bool ShiftObjectsManager::IsGoodNeutrino(const shared_ptr<HepMCParticle> particle, const shared_ptr<PhysicsObjects> &allParticles) {
  if (fabs(particle->GetPid()) != 12 && fabs(particle->GetPid()) != 14 && fabs(particle->GetPid()) != 16) return false;
  if (!hepMCProcessor->IsLastCopy(particle, allParticles)) return false;
  return true;
}

void ShiftObjectsManager::InsertGoodZprimesCollection(shared_ptr<Event> event) {
  auto particles = event->GetCollection("IndexedParticles");

  auto goodZprimes = make_shared<PhysicsObjects>();

  for (int particleIndex = 0; particleIndex < particles->size(); particleIndex++) {
    auto physicsObject = particles->at(particleIndex);
    auto hepMCParticle = asHepMCParticle(physicsObject);
    if (!IsGoodZprime(hepMCParticle, particles)) continue;
    goodZprimes->push_back(physicsObject);
  }
  event->AddCollection("goodZprimes", goodZprimes);
}

void ShiftObjectsManager::InsertGoodDarkPhotonsCollection(shared_ptr<Event> event) {
  auto particles = event->GetCollection("IndexedParticles");

  auto goodDarkPhotons = make_shared<PhysicsObjects>();

  for (int particleIndex = 0; particleIndex < particles->size(); particleIndex++) {
    auto physicsObject = particles->at(particleIndex);
    auto hepMCParticle = asHepMCParticle(physicsObject);

    if (!IsGoodDarkPhoton(hepMCParticle, particles)) {
      continue;
    }

    goodDarkPhotons->push_back(physicsObject);
  }
  event->AddCollection("goodDarkPhotons", goodDarkPhotons);
}

void ShiftObjectsManager::InsertGoodDarkHadronsCollection(shared_ptr<Event> event) {
  auto particles = event->GetCollection("IndexedParticles");

  auto goodDarkHadrons = make_shared<PhysicsObjects>();

  for (int particleIndex = 0; particleIndex < particles->size(); particleIndex++) {
    auto physicsObject = particles->at(particleIndex);
    auto hepMCParticle = asHepMCParticle(physicsObject);
    if (!IsGoodDarkHadron(hepMCParticle, particles)) continue;

    goodDarkHadrons->push_back(physicsObject);
  }
  event->AddCollection("goodDarkHadrons", goodDarkHadrons);
}

void ShiftObjectsManager::InsertGoodMuonsCollection(shared_ptr<Event> event) {
  auto particles = event->GetCollection("IndexedParticles");

  auto goodMuons = make_shared<PhysicsObjects>();

  for (int particleIndex = 0; particleIndex < particles->size(); particleIndex++) {
    auto physicsObject = particles->at(particleIndex);
    auto hepMCParticle = asHepMCParticle(physicsObject);
    if (!IsGoodMuon(hepMCParticle, particles)) continue;

    goodMuons->push_back(physicsObject);
  }
  event->AddCollection("goodMuons", goodMuons);
}

void ShiftObjectsManager::InsertNeutrinosCollection(shared_ptr<Event> event) {
  auto particles = event->GetCollection("IndexedParticles");

  auto neutrinos = make_shared<PhysicsObjects>();

  for (int particleIndex = 0; particleIndex < particles->size(); particleIndex++) {
    auto physicsObject = particles->at(particleIndex);
    auto hepMCParticle = asHepMCParticle(physicsObject);
    if (!IsGoodNeutrino(hepMCParticle, particles)) continue;

    neutrinos->push_back(physicsObject);
  }
  event->AddCollection("goodNeutrinos", neutrinos);
}

void ShiftObjectsManager::InsertMuonsHittingDetectorCollection(shared_ptr<Event> event, string variant, shared_ptr<map<string, int>> nMuons) {
  auto goodMuons = event->GetCollection("goodMuons");
  auto passingMuons = make_shared<PhysicsObjects>();
  auto allParticles = event->GetCollection("IndexedParticles");

  for (auto physicsObject : *goodMuons) {
    auto hepMCParticle = asHepMCParticle(physicsObject);
    if (nMuons) nMuons->at("1_hasMuons")++;

    float recoVariable = hepMCParticle->GetLorentzVector().E();
    if (variant == "cmsPT") {
      recoVariable = hepMCParticle->GetLorentzVector().Pt();
    }

    // Check that the muon has at least 30 GeV of energy (or pT in case of CMS), so that it can trigger and be reconstructed at CMS
    if (recoVariable < 30) continue;
    if (nMuons) nMuons->at("2_triggerAndReco")++;

    // Check that they intersect with the detector
    if (!detector->DoesParticleGoThrough(hepMCParticle)) continue;
    if (nMuons) nMuons->at("3_intersectingDetector")++;

    // Check that the production vertex is before the detector
    if (!detector->IsProductionVertexBeforeTheEnd(hepMCParticle, 2.0)) continue;
    if (nMuons) nMuons->at("4_beforeDetector")++;

    // Check that the muon goes through the rock
    if (!detector->DoesParticleGoThroughRock(hepMCParticle, allParticles)) continue;
    if (nMuons) nMuons->at("5_throughRock")++;

    passingMuons->push_back(physicsObject);
  }

  event->AddCollection("muonsInDetector", passingMuons);
}

void ShiftObjectsManager::InsertNeutrinosHittingDetectorCollection(shared_ptr<Event> event, shared_ptr<map<string, int>> nNeutrinos) {
  auto goodNeutrinos = event->GetCollection("goodNeutrinos");
  auto passingNeutrinos = make_shared<PhysicsObjects>();
  auto allParticles = event->GetCollection("IndexedParticles");

  for (auto physicsObject : *goodNeutrinos) {
    auto hepMCParticle = asHepMCParticle(physicsObject);
    if (nNeutrinos) nNeutrinos->at("1_hasNeutrinos")++;

    // Check that they intersect with the detector
    if (!detector->DoesParticleGoThrough(hepMCParticle)) continue;
    if (nNeutrinos) nNeutrinos->at("2_intersectingDetector")++;

    // Check that the production vertex is before the detector
    // if (!detector->IsProductionVertexBeforeTheEnd(hepMCParticle, 2.0)) continue;
    if (nNeutrinos) nNeutrinos->at("3_beforeDetector")++;

    passingNeutrinos->push_back(physicsObject);
  }

  event->AddCollection("neutrinosInDetector", passingNeutrinos);
}