#include "ShiftObjectsManager.hpp"

#include "ConfigManager.hpp"
#include "Logger.hpp"
#include "ShiftDetector.hpp"

using namespace std;

ShiftObjectsManager::ShiftObjectsManager() {
  auto &config = ConfigManager::GetInstance();

  hepMCProcessor = make_unique<HepMCProcessor>();
  //   config.GetMap("detectorParams", detectorParams);
  //   config.GetMap("caloEtaEdges", caloEtaEdges);
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

void ShiftObjectsManager::InsertGoodZprimesCollection(shared_ptr<Event> event) {
  auto particles = event->GetCollection("Particle");

  auto goodZprimes = make_shared<PhysicsObjects>();

  for (int particleIndex = 0; particleIndex < particles->size(); particleIndex++) {
    auto physicsObject = particles->at(particleIndex);
    physicsObject->SetIndex(particleIndex);
    auto hepMCParticle = asHepMCParticle(physicsObject);
    if (!IsGoodZprime(hepMCParticle, particles)) continue;
    goodZprimes->push_back(physicsObject);
  }
  event->AddCollection("goodZprimes", goodZprimes);
}

void ShiftObjectsManager::InsertGoodDarkPhotonsCollection(shared_ptr<Event> event) {
  auto particles = event->GetCollection("Particle");

  auto goodDarkPhotons = make_shared<PhysicsObjects>();

  for (int particleIndex = 0; particleIndex < particles->size(); particleIndex++) {
    auto physicsObject = particles->at(particleIndex);
    physicsObject->SetIndex(particleIndex);
    auto hepMCParticle = asHepMCParticle(physicsObject);
    if (!IsGoodDarkPhoton(hepMCParticle, particles)) continue;
    goodDarkPhotons->push_back(physicsObject);
  }
  event->AddCollection("goodDarkPhotons", goodDarkPhotons);
}

void ShiftObjectsManager::InsertGoodDarkHadronsCollection(shared_ptr<Event> event) {
  auto particles = event->GetCollection("Particle");

  auto goodDarkHadrons = make_shared<PhysicsObjects>();

  for (int particleIndex = 0; particleIndex < particles->size(); particleIndex++) {
    auto physicsObject = particles->at(particleIndex);
    physicsObject->SetIndex(particleIndex);
    auto hepMCParticle = asHepMCParticle(physicsObject);
    if (!IsGoodDarkHadron(hepMCParticle, particles)) continue;

    goodDarkHadrons->push_back(physicsObject);
  }
  event->AddCollection("goodDarkHadrons", goodDarkHadrons);
}

void ShiftObjectsManager::InsertGoodMuonsCollection(shared_ptr<Event> event) {
  auto particles = event->GetCollection("Particle");

  auto goodMuons = make_shared<PhysicsObjects>();

  for (int particleIndex = 0; particleIndex < particles->size(); particleIndex++) {
    auto physicsObject = particles->at(particleIndex);
    physicsObject->SetIndex(particleIndex);
    auto hepMCParticle = asHepMCParticle(physicsObject);
    if (!IsGoodMuon(hepMCParticle, particles)) continue;

    goodMuons->push_back(physicsObject);
  }
  event->AddCollection("goodMuons", goodMuons);
}

void ShiftObjectsManager::InsertMuonsHittingDetectorCollection(shared_ptr<Event> event, const map<string, float> &detectorParams,
                                                               shared_ptr<map<string, int>> nMuons) {
  auto goodMuons = event->GetCollection("goodMuons");
  auto detector = make_shared<ShiftDetector>(detectorParams);
  auto passingMuons = make_shared<PhysicsObjects>();

  for (auto physicsObject : *goodMuons) {
    auto hepMCParticle = asHepMCParticle(physicsObject);
    if (nMuons) nMuons->at("1_hasMuons")++;

    // Check that the muon has at least 30 GeV of energy, so that it can trigger and be reconstructed at CMS
    if (hepMCParticle->GetLorentzVector().E() < 30) continue;
    if (nMuons) nMuons->at("2_triggerAndReco")++;

    // Check that they intersect with the detector
    if (!detector->DoesParticleGoThrough(hepMCParticle)) continue;
    if (nMuons) nMuons->at("3_intersectingDetector")++;

    // Check that the production vertex is before the detector
    if (!detector->IsProductionVertexBeforeTheEnd(hepMCParticle, 2.0)) continue;
    if (nMuons) nMuons->at("4_beforeDetector")++;

    // Check that the muon goes through the rock
    if (!detector->DoesParticleGoThroughRock(hepMCParticle)) continue;
    if (nMuons) nMuons->at("5_throughRock")++;

    passingMuons->push_back(physicsObject);
  }

  event->AddCollection("muonsInDetector", passingMuons);
}
