#include "ShiftObjectsManager.hpp"

#include "ConfigManager.hpp"
#include "Logger.hpp"

using namespace std;

ShiftObjectsManager::ShiftObjectsManager() {
  auto& config = ConfigManager::GetInstance();

    hepMCProcessor = make_unique<HepMCProcessor>();
//   config.GetMap("detectorParams", detectorParams);
//   config.GetMap("caloEtaEdges", caloEtaEdges);
}

bool ShiftObjectsManager::IsGoodZprime(const shared_ptr<HepMCParticle> particle, const shared_ptr<PhysicsObjects> &allParticles) {
  if(particle->GetPid() != 4900023) return false;
  if(!hepMCProcessor->IsLastCopy(particle, allParticles)) return false;
  return true;
}

bool ShiftObjectsManager::IsGoodDarkHadron(const shared_ptr<HepMCParticle> particle, const shared_ptr<PhysicsObjects> &allParticles) {
  if(fabs(particle->GetPid()) != 4900111 && fabs(particle->GetPid()) != 4900113) return false;
  if(!hepMCProcessor->IsLastCopy(particle, allParticles)) return false;
  return true;
}

bool ShiftObjectsManager::IsGoodMuonFromDarkHadron(const shared_ptr<HepMCParticle> particle, const shared_ptr<PhysicsObjects> &allParticles) {
  if(fabs(particle->GetPid()) != 13) return false;
  if(!hepMCProcessor->IsLastCopy(particle, allParticles)) return false;
  if(!particle->FirstNonCopyMotherWithPid(4900111, allParticles) && !particle->FirstNonCopyMotherWithPid(4900113, allParticles)) return false;
  return true;
}

void ShiftObjectsManager::InsertGoodZprimesCollection(shared_ptr<Event> event) {
  auto particles = event->GetCollection("Particle");
  
  auto goodZprimes = make_shared<PhysicsObjects>();
  
  for (int particleIndex=0; particleIndex < particles->size(); particleIndex++){
    auto physicsObject = particles->at(particleIndex);
    auto hepMCParticle = asHepMCParticle(physicsObject, particleIndex, 100);
    if (!IsGoodZprime(hepMCParticle, particles)) continue;
    goodZprimes->push_back(physicsObject);
  }
  event->AddCollection("goodZprimes", goodZprimes);
}

void ShiftObjectsManager::InsertGoodDarkHadronsCollection(shared_ptr<Event> event) {
  auto particles = event->GetCollection("Particle");
  
  auto goodDarkHadrons = make_shared<PhysicsObjects>();
  
  for (int particleIndex=0; particleIndex < particles->size(); particleIndex++){
    auto physicsObject = particles->at(particleIndex);
    auto hepMCParticle = asHepMCParticle(physicsObject, particleIndex, 100);
    if (!IsGoodDarkHadron(hepMCParticle, particles)) continue;
    goodDarkHadrons->push_back(physicsObject);
  }
  event->AddCollection("goodDarkHadrons", goodDarkHadrons);
}

void ShiftObjectsManager::InsertGoodMuonsFromDarkHadronsCollection(shared_ptr<Event> event) {
  auto particles = event->GetCollection("Particle");
  
  auto goodMuonsFromDarkHadrons = make_shared<PhysicsObjects>();
  
  for (int particleIndex=0; particleIndex < particles->size(); particleIndex++){
    auto physicsObject = particles->at(particleIndex);
    auto hepMCParticle = asHepMCParticle(physicsObject, particleIndex, 100);
    if (!IsGoodMuonFromDarkHadron(hepMCParticle, particles)) continue;
    goodMuonsFromDarkHadrons->push_back(physicsObject);
  }
  event->AddCollection("goodMuonsFromDarkHadrons", goodMuonsFromDarkHadrons);
}