#include "HepMCParticle.hpp"
#include "Logger.hpp"

class ShiftDetector {
  // Class to describe a spherical detector located at (x,y,z) coordinates with a given radius
 public:
  ShiftDetector(const std::map<std::string, float> &params);
  ~ShiftDetector() {}

  void Print();

  bool DoesParticleGoThrough(const std::shared_ptr<HepMCParticle> &particle);
  bool IsProductionVertexBeforeTheEnd(const std::shared_ptr<HepMCParticle> &particle, float maxDistanceInsideDetector = 0.0);
  bool DoesParticleGoThroughRock(const std::shared_ptr<HepMCParticle> &particle);

 private:
  float x, y, z, outer_radius, inner_radius, total_length;  // (m)
  bool forcedLHCring = false;

  TRotation rotation;
  TVector3 translation;
};
