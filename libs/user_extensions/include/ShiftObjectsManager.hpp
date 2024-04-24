#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "Helpers.hpp"
#include "HepMCProcessor.hpp"
#include "UserExtensionsHelpers.hpp"

class ShiftObjectsManager {
 public:
  ShiftObjectsManager();
  ~ShiftObjectsManager() = default;

  void InsertGoodZprimesCollection(std::shared_ptr<Event> event);
  void InsertGoodDarkHadronsCollection(std::shared_ptr<Event> event);
  void InsertGoodMuonsCollection(std::shared_ptr<Event> event);

  void InsertMuonsHittingDetectorCollection(std::shared_ptr<Event> event, const std::map<std::string, float> &detectorParams,
                                            std::shared_ptr<std::map<std::string, int>> nMuons=nullptr);

 private:
  bool IsGoodZprime(const std::shared_ptr<HepMCParticle> particle, const std::shared_ptr<PhysicsObjects> &allParticles);
  bool IsGoodDarkHadron(const std::shared_ptr<HepMCParticle> particle, const std::shared_ptr<PhysicsObjects> &allParticles);
  bool IsGoodMuon(const std::shared_ptr<HepMCParticle> particle, const std::shared_ptr<PhysicsObjects> &allParticles);

  std::unique_ptr<HepMCProcessor> hepMCProcessor;
};
