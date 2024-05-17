#include "HepMCParticle.hpp"
#include "Logger.hpp"

class ShiftDetector {
  // Class to describe a spherical detector located at (x,y,z) coordinates with a given radius
 public:
  ShiftDetector(const std::map<std::string, float> &params, bool isLHCb_);
  ~ShiftDetector() {}

  void Print();

  bool DoesParticleGoThrough(const std::shared_ptr<HepMCParticle> &particle);
  bool IsProductionVertexBeforeTheEnd(const std::shared_ptr<HepMCParticle> &particle, float maxDistanceInsideDetector = 0.0);
  bool DoesParticleGoThroughRock(const std::shared_ptr<HepMCParticle> &particle);

 private:
  bool IsWithinLHCbAcceptance(const std::shared_ptr<HepMCParticle> &particle);

  float x, y, z, outer_radius, inner_radius, total_length;  // (m)
  float minLength, maxLength, minEta, maxEta, maxDistance; // (m), for LHCb case
  bool forcedLHCring = false;
  bool isLHCb;

  TRotation rotation;
  TVector3 translation;
};
