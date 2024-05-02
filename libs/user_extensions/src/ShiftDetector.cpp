#include "ShiftDetector.hpp"

using namespace std;

ShiftDetector::ShiftDetector(const std::map<std::string, float> &params) {
  x = params.at("x");
  y = params.at("y");
  z = params.at("z");
  radius = params.at("radius");
  maxEta = params.at("maxEta");

  if (x < 0) {
    forcedLHCring = true;
    float radius = 4300;  // [m]
    float x_1 = sqrt(pow(radius, 2) - pow(z, 2)) + radius;
    float x_2 = -sqrt(pow(radius, 2) - pow(z, 2)) + radius;
    x = min(x_1, x_2);
  }
}

void ShiftDetector::Print() {
  info() << "\n\n--------------------------------------------------" << std::endl;
  info() << "Detector at: (" << x << ", " << y << ", " << z << ") with radius: " << radius << std::endl;
  // calculate the fraction of the solid angle the detector covers
  info() << "Angular coverage: " << 2 * atan(radius / sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2))) << std::endl;
  info() << "Forced to be on the LHC ring: " << (forcedLHCring ? "yes" : "no") << std::endl;
  info() << "--------------------------------------------------\n\n" << std::endl;
}

bool ShiftDetector::DoesParticleGoThrough(const shared_ptr<HepMCParticle> &particle) {
  // check if the particle, given it's eta and phi, as well as production vertex x,y,z, passes through this sphere

  auto fourVector = particle->GetLorentzVector();
  float eta = fourVector.Eta();
  float theta = 2 * atan(exp(-eta));
  float phi = fourVector.Phi();
  float pT = fourVector.Pt();
  float x_p = particle->GetX() / 1e3;  // convert mm to m
  float y_p = particle->GetY() / 1e3;  // convert mm to m
  float z_p = particle->GetZ() / 1e3;  // convert mm to m

  // Calculate velocity components
  double v_x = pT * cos(phi);
  double v_y = pT * sin(phi);
  double v_z = pT * sinh(eta);

  // Calculate vector from particle start to sphere center
  double dx = x - x_p;
  double dy = y - y_p;
  double dz = z - z_p;

  // Quadratic equation coefficients for sphere intersection
  double a = v_x * v_x + v_y * v_y + v_z * v_z;
  double b = 2 * (dx * v_x + dy * v_y + dz * v_z);
  double c = dx * dx + dy * dy + dz * dz - radius * radius;

  //   // check if production vertex is within the detector:
  bool insideDetector = sqrt(dx * dx + dy * dy + dz * dz) < radius;
  if (insideDetector) {
    warn() << "Production vertex inside the detector" << endl;
    return fabs(eta) < maxEta;
  }

  //   // Dot product of velocity vector and vector to sphere center
  double dotProduct = v_x * dx + v_y * dy + v_z * dz;
  if (dotProduct <= 0) {
    warn() << "Wrong direction" << endl;
    // Particle is moving away from or perpendicular to the direction of the sphere
    return false;
  }

  double discriminant = b * b - 4 * a * c;
  if (discriminant < 0) {
    return false;
  }

  // Intersection points (t solutions)
  double t1 = (-b + std::sqrt(discriminant)) / (2 * a);
  double t2 = (-b - std::sqrt(discriminant)) / (2 * a);

  double inter_1_x = t1 * v_x;
  double inter_1_y = t1 * v_y;
  double inter_1_z = t1 * v_z;
  double inter_2_x = t2 * v_x;
  double inter_2_y = t2 * v_y;
  double inter_2_z = t2 * v_z;

  // Calculate the angle theta_cyl corresponding to eta
  double theta_cyl = 2 * std::atan(std::exp(-maxEta));

  // Radius of the cylindrical hole
  double R_cyl = radius * std::sin(theta_cyl);

  // Tangent direction at the circle point
  double alpha = std::atan2(y, x);
  double tx = std::cos(alpha + M_PI / 2);
  double ty = std::sin(alpha + M_PI / 2);

  // Check if these points fall outside the cylindrical hole
  double radius1 = std::sqrt(inter_1_x * inter_1_x + inter_1_y * inter_1_y);
  double radius2 = std::sqrt(inter_2_x * inter_2_x + inter_2_y * inter_2_y);

  // Radius of the cylindrical hole
  double R_cyl1 = std::sqrt(inter_1_x * tx + inter_1_y * ty);
  double R_cyl2 = std::sqrt(inter_2_x * tx + inter_2_y * ty);

  if (radius1 > R_cyl1) {
    return true;
  }

  if (radius2 > R_cyl2) {
    return true;
  }
  return false;
}

// bool ShiftDetector::DoesParticleGoThrough(const shared_ptr<HepMCParticle> &particle) {
//   // check if the particle, given it's eta and phi, as well as production vertex x,y,z, passes through this sphere

//   auto fourVector = particle->GetLorentzVector();
//   float eta = fourVector.Eta();
//   float theta = 2 * atan(exp(-eta));
//   float phi = fourVector.Phi();
//   float pT = fourVector.Pt();
//   float x_p = particle->GetX() / 1e3;  // convert mm to m
//   float y_p = particle->GetY() / 1e3;  // convert mm to m
//   float z_p = particle->GetZ() / 1e3;  // convert mm to m

//   // Calculate velocity components
//   double v_x = pT * cos(phi);
//   double v_y = pT * sin(phi);
//   double v_z = pT * sinh(eta);

//   // Calculate vector from particle start to sphere center
//   double dx = x - x_p;
//   double dy = y - y_p;
//   double dz = z - z_p;

//   // check if production vertex is within the detector:
//   bool insideDetector = sqrt(dx * dx + dy * dy + dz * dz) < radius;
//   if(insideDetector) {
//     return true;
//   }

//   // Dot product of velocity vector and vector to sphere center
//   double dotProduct = v_x * dx + v_y * dy + v_z * dz;
//   if (dotProduct <= 0) {
//     warn() << "Wrong direction" << endl;
//     // Particle is moving away from or perpendicular to the direction of the sphere
//     return false;
//   }

//   // Coefficients of the quadratic equation At^2 + Bt + C = 0
//   double A = v_x * v_x + v_y * v_y + v_z * v_z;
//   double B = 2 * dotProduct;
//   double C = dx * dx + dy * dy + dz * dz - radius * radius;

//   // Calculate discriminant
//   double discriminant = B * B - 4 * A * C;

//   // Check if there is an intersection
//   return discriminant >= 0;
// }

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

  float distanceToDetectorCenter = sqrt(pow(xProd - x, 2) + pow(yProd - y, 2) + pow(zProd - z, 2));
  float distanceToDetector = distanceToDetectorCenter - radius;

  float particleEnergy = particle->GetLorentzVector().E();

  return particleEnergy > distanceToDetector;
}