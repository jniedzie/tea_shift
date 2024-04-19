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

bool ShiftObjectsManager::IsGoodZprime(const shared_ptr<HepMCParticle> particle, int particleIndex, const shared_ptr<PhysicsObjects> &allParticles) {
  if(particle->GetPid() != 4900023) return false;
  if(!hepMCProcessor->IsLastCopy(particle, particleIndex, allParticles)) return false;
  return true;
}

bool ShiftObjectsManager::IsGoodDarkHadron(const shared_ptr<HepMCParticle> particle, int particleIndex, const shared_ptr<PhysicsObjects> &allParticles) {
  if(fabs(particle->GetPid()) != 4900111 && fabs(particle->GetPid()) != 4900113) return false;
  if(!hepMCProcessor->IsLastCopy(particle, particleIndex, allParticles)) return false;
  return true;
}

void ShiftObjectsManager::InsertGoodZprimesCollection(shared_ptr<Event> event) {
  auto particles = event->GetCollection("Particle");
  
  auto goodZprimes = make_shared<PhysicsObjects>();
  
  for (int particleIndex=0; particleIndex < particles->size(); particleIndex++){
    auto physicsObject = particles->at(particleIndex);
    auto hepMCParticle = asHepMCParticle(physicsObject);
    if (!IsGoodZprime(hepMCParticle, particleIndex, particles)) continue;
    goodZprimes->push_back(physicsObject);
  }
  event->AddCollection("goodZprimes", goodZprimes);
}

void ShiftObjectsManager::InsertGoodDarkHadronsCollection(shared_ptr<Event> event) {
  auto particles = event->GetCollection("Particle");
  
  auto goodDarkHadrons = make_shared<PhysicsObjects>();
  
  for (int particleIndex=0; particleIndex < particles->size(); particleIndex++){
    auto physicsObject = particles->at(particleIndex);
    auto hepMCParticle = asHepMCParticle(physicsObject);
    if (!IsGoodDarkHadron(hepMCParticle, particleIndex, particles)) continue;
    goodDarkHadrons->push_back(physicsObject);
  }
  event->AddCollection("goodDarkHadrons", goodDarkHadrons);
}