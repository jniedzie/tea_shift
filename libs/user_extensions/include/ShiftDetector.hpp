#include "HepMCParticle.hpp"
#include "Logger.hpp"

class ShiftDetector {
  // Class to describe a spherical detector located at (x,y,z) coordinates with a given radius
 public:
  ShiftDetector(const std::map<std::string, float> &params) {
    x = params.at("x");
    y = params.at("y");
    z = params.at("z");
    radius = params.at("radius");

    if (z < 0) {
      forcedLHCring = true;
      float radius = 4300;  // [m]
      z = sqrt(pow(radius,2) - pow(x - radius,2));
    }
  }
  ~ShiftDetector() {}

  void Print() {
    info() << "\n\n--------------------------------------------------" << std::endl;
    info() << "Detector at: (" << x << ", " << y << ", " << z << ") with radius: " << radius << std::endl;
    info() << "Forced to be on the LHC ring: " << (forcedLHCring ? "yes" : "no") << std::endl;
    info() << "--------------------------------------------------\n\n" << std::endl;
  }

  bool DoesParticleGoThrough(const std::shared_ptr<HepMCParticle> &particle);
  bool IsProductionVertexBeforeTheEnd(const std::shared_ptr<HepMCParticle> &particle, float maxDistanceInsideDetector = 0.0);
  bool DoesParticleGoThroughRock(const std::shared_ptr<HepMCParticle> &particle);

 private:
  float x, y, z, radius;  // Coordinates of the detector and its radius (m)
  bool forcedLHCring = false;
};