#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "Helpers.hpp"
#include "UserExtensionsHelpers.hpp"
#include "HepMCProcessor.hpp"

class ShiftObjectsManager {
 public:
  ShiftObjectsManager();
  ~ShiftObjectsManager() = default;

  void InsertGoodZprimesCollection(std::shared_ptr<Event> event);

 private:
  bool IsGoodZprime(const std::shared_ptr<HepMCParticle> particle, int particleIndex, const std::shared_ptr<PhysicsObjects> &allParticles);

  std::unique_ptr<HepMCProcessor> hepMCProcessor;
  
  
//   std::map<std::string, float> detectorParams, caloEtaEdges;
};
