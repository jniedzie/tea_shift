#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "Helpers.hpp"
#include "HepMCProcessor.hpp"
#include "UserExtensionsHelpers.hpp"
#include "ShiftDetector.hpp"

class ShiftObjectsManager {
 public:
  ShiftObjectsManager(const std::map<std::string, float> &detectorParams, std::string variant);
  ~ShiftObjectsManager() = default;

  void InsertIndexedParticles(std::shared_ptr<Event> event);

  void InsertGoodZprimesCollection(std::shared_ptr<Event> event);
  void InsertGoodDarkHadronsCollection(std::shared_ptr<Event> event);
  void InsertGoodMuonsCollection(std::shared_ptr<Event> event);
  void InsertGoodDarkPhotonsCollection(std::shared_ptr<Event> event);

  void InsertNeutrinosCollection(std::shared_ptr<Event> event);

  void InsertMuonsHittingDetectorCollection(std::shared_ptr<Event> event, std::string variant, std::shared_ptr<std::map<std::string, int>> nMuons = nullptr);
  void InsertNeutrinosHittingDetectorCollection(std::shared_ptr<Event> event, std::shared_ptr<std::map<std::string, int>> nNeutrinos);

 private:
  std::unique_ptr<ShiftDetector> detector;

  bool IsGoodZprime(const std::shared_ptr<HepMCParticle> particle, const std::shared_ptr<PhysicsObjects> &allParticles);
  bool IsGoodDarkHadron(const std::shared_ptr<HepMCParticle> particle, const std::shared_ptr<PhysicsObjects> &allParticles);
  bool IsGoodMuon(const std::shared_ptr<HepMCParticle> particle, const std::shared_ptr<PhysicsObjects> &allParticles);
  bool IsGoodDarkPhoton(const std::shared_ptr<HepMCParticle> particle, const std::shared_ptr<PhysicsObjects> &allParticles);
  bool IsGoodNeutrino(const std::shared_ptr<HepMCParticle> particle, const std::shared_ptr<PhysicsObjects> &allParticles);

  std::unique_ptr<HepMCProcessor> hepMCProcessor;
};
