#include "ShiftDetector.hpp"

using namespace std;

ShiftDetector::ShiftDetector(const std::map<std::string, float> &params) {
  x = params.at("x");
  y = params.at("y");
  z = params.at("z");
  radius = params.at("radius");

  if (z < 0) {
    forcedLHCring = true;
    float radius = 4300;  // [m]
    z = sqrt(pow(radius, 2) - pow(x - radius, 2));
  }
}

void ShiftDetector::Print() {
  info() << "\n\n--------------------------------------------------" << std::endl;
  info() << "Detector at: (" << x << ", " << y << ", " << z << ") with radius: " << radius << std::endl;
  info() << "Forced to be on the LHC ring: " << (forcedLHCring ? "yes" : "no") << std::endl;
  info() << "--------------------------------------------------\n\n" << std::endl;
}

bool ShiftDetector::DoesParticleGoThrough(const shared_ptr<HepMCParticle> &particle) {
  // check if the particle, given it's eta and phi, as well as production vertex x,y,z, passes through this sphere (ignore the magnetic
  // field)
  auto fourVector = particle->GetLorentzVector();
  float eta = fourVector.Eta();
  float theta = 2 * atan(exp(-eta));
  float phi = fourVector.Phi();
  float xProd = particle->GetX() / 1e3;  // convert mm to m
  float yProd = particle->GetY() / 1e3;  // convert mm to m
  float zProd = particle->GetZ() / 1e3;  // convert mm to m

  // Direction vector components
  double dx = cos(phi) * sin(theta);
  double dy = sin(phi) * sin(theta);
  double dz = cos(theta);

  // Calculate coefficients of the quadratic equation
  double a = dx * dx + dy * dy + dz * dz;
  double b = 2 * (dx * (xProd - x) + dy * (yProd - y) + dz * (zProd - z));
  double c = (xProd - x) * (xProd - x) + (yProd - y) * (yProd - y) + (zProd - z) * (zProd - z) - radius * radius;

  // Calculate the discriminant
  double discriminant = b * b - 4 * a * c;

  // Check if the discriminant is non-negative
  return discriminant >= 0;
}

bool ShiftDetector::IsProductionVertexBeforeTheEnd(const shared_ptr<HepMCParticle> &particle, float maxDistanceInsideDetector) {
  // check if the production vertex of the particle is before the detector, or at most 1m past the detector's center

  float xProd = particle->GetX() / 1e3;  // convert mm to m
  float yProd = particle->GetY() / 1e3;  // convert mm to m
  float zProd = particle->GetZ() / 1e3;  // convert mm to m

  float particleDistance = sqrt(pow(xProd, 2) + pow(yProd, 2) + pow(zProd, 2));
  float detectorDistance = sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2));
  return particleDistance < detectorDistance + maxDistanceInsideDetector;
}

bool ShiftDetector::DoesParticleGoThroughRock(const shared_ptr<HepMCParticle> &particle) {
  // calculate the distance the particle has to travel from production vertex to the edge of the detector
  float xProd = particle->GetX() / 1e3;  // convert mm to m
  float yProd = particle->GetY() / 1e3;  // convert mm to m
  float zProd = particle->GetZ() / 1e3;  // convert mm to m

  float particleDistance = sqrt(pow(xProd, 2) + pow(yProd, 2) + pow(zProd, 2));
  float detectorDistance = sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2));
  float distanceToDetector = detectorDistance - particleDistance - radius;

  float particleEnergy = particle->GetLorentzVector().E();

  return particleEnergy > distanceToDetector;
}