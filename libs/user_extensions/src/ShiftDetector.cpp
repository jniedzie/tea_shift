#include "ShiftDetector.hpp"

using namespace std;

ShiftDetector::ShiftDetector(const std::map<std::string, float> &params)
{
  x = params.at("x");
  y = params.at("y");
  z = params.at("z");
  outer_radius = params.at("radius");
  total_length = params.at("length");
  double maxEta = params.at("maxEta");

  double theta_inner = 2 * std::atan(std::exp(-2.4));
  inner_radius = outer_radius * std::sin(theta_inner);

  if (y < 0) {
    forcedLHCring = true;
    float outer_radius = 4300;  // [m]
    float y_1 = sqrt(pow(outer_radius, 2) - pow(x, 2)) + outer_radius;
    float y_2 = -sqrt(pow(outer_radius, 2) - pow(x, 2)) + outer_radius;
    y = min(y_1, y_2);
  }

  double theta = TMath::ATan2(y, x);
  rotation.RotateY(theta);
  
  TVector3 detectorCenter(x, y ,z);
  
  auto newCenter = detectorCenter;
  newCenter *= rotation;
  translation = -newCenter;
}

void ShiftDetector::Print() {
  info() << "\n\n--------------------------------------------------" << endl;
  info() << "Detector at: (" << x << ", " << y << ", " << z << ") with radius: " << outer_radius << " and length: " << total_length << endl;
  // calculate the fraction of the solid angle the detector covers
  float distance = sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2));
  float fullArea = 4 * TMath::Pi() * distance * distance;
  float detectorArea = TMath::Pi() * outer_radius * outer_radius;
  info() << "Angular coverage: " << detectorArea/fullArea << endl;
  info() << "Forced to be on the LHC ring: " << (forcedLHCring ? "yes" : "no") << endl;
  info() << "--------------------------------------------------\n\n" << endl;
}

bool ShiftDetector::DoesParticleGoThrough(const shared_ptr<HepMCParticle> &particle) {
  
  // convert mm to m. x is our y, y is our z, z is our x
  TVector3 origin(particle->GetZ() / 1e3, particle->GetX() / 1e3, particle->GetY() / 1e3);

  auto fourVector = particle->GetLorentzVector();
  float eta = fourVector.Eta();
  float phi = fourVector.Phi();
  TVector3 direction(std::sinh(eta), std::cos(phi), std::sin(phi));

  origin *= rotation;
  origin += translation;
  direction *= rotation;

  if (direction.Mag() == 0) {
    warn() << "Direction vector is zero, invalid input." << endl;
    return false;
  }

  TVector3 unitDirection = direction.Unit();

  // Check radial direction, ensuring it's pointing towards the cylinder if outside
  TVector3 radialOrigin(origin.Y(), origin.Z(), 0);
  TVector3 radialDirection(unitDirection.Y(), unitDirection.Z(), 0);
  if (radialOrigin.Mag() > outer_radius) {
    if (radialOrigin.Dot(radialDirection) > 0) {
      return false;  // Moving away from the cylinder radially
    }
  }

  // Check z-direction, ensuring it's pointing towards the cylinder if outside
  if ((origin.X() > total_length / 2 && unitDirection.X() > 0) || (origin.X() < -total_length / 2 && unitDirection.X() < 0)) {
    return false;  // Moving away from the cylinder along the z-axis
  }

  // Endcap intersection checks
  double x1 = -total_length / 2 - origin.X();
  double x2 = total_length / 2 - origin.X();
  double t1 = x1 / unitDirection.X();
  double t2 = x2 / unitDirection.X();

  // Check if t1 and t2 result in intersections within the outer and inner radius
  for (double t : {t1, t2}) {
    if (t >= 0) {  // Only consider t >= 0 for valid intersection direction
      TVector3 intersectionPoint = origin + t * unitDirection;
      double radialDistance = TMath::Sqrt(intersectionPoint.Y() * intersectionPoint.Y() + intersectionPoint.Z() * intersectionPoint.Z());
      if (radialDistance >= inner_radius && radialDistance <= outer_radius) {
        return true;
      }
    }
  }

  double a = unitDirection.Y() * unitDirection.Y() + unitDirection.Z() * unitDirection.Z();
  double b = 2 * (origin.Y() * unitDirection.Y() + origin.Z() * unitDirection.Z());
  double c = origin.Y() * origin.Y() + origin.Z() * origin.Z() - outer_radius * outer_radius;
  double discriminant = b * b - 4 * a * c;

  if (discriminant >= 0) {  // Potential intersection with the cylinder's sides
    double t3 = (-b - TMath::Sqrt(discriminant)) / (2 * a);
    double t4 = (-b + TMath::Sqrt(discriminant)) / (2 * a);

    for (double t : {t3, t4}) {
      if (t >= 0) {
        TVector3 intersectionPoint = origin + t * unitDirection;
        double x = intersectionPoint.X();
        if (x >= -total_length / 2 && x <= total_length / 2) {
          return true;
        }
      }
    }
  }
  
  return false;
}

bool ShiftDetector::IsProductionVertexBeforeTheEnd(const shared_ptr<HepMCParticle> &particle, float maxDistanceInsideDetector) {
  // check if the production vertex of the particle is before the detector, or at most 1m past the detector's center
  // convert mm to m. x is our y, y is our z, z is our x
  float xProd = particle->GetZ() / 1e3;
  float yProd = particle->GetX() / 1e3;
  float zProd = particle->GetY() / 1e3;

  float particleDistance = sqrt(pow(xProd, 2) + pow(yProd, 2) + pow(zProd, 2));
  float detectorDistance = sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2));
  return particleDistance < detectorDistance + maxDistanceInsideDetector;
}

bool ShiftDetector::DoesParticleGoThroughRock(const shared_ptr<HepMCParticle> &particle) {
  // calculate the distance the particle has to travel from production vertex to the edge of the detector
  // convert mm to m. x is our y, y is our z, z is our x
  float xProd = particle->GetZ() / 1e3;
  float yProd = particle->GetX() / 1e3;
  float zProd = particle->GetY() / 1e3;

  float distanceToDetectorCenter = sqrt(pow(xProd - x, 2) + pow(yProd - y, 2) + pow(zProd - z, 2));
  float distanceToDetector = distanceToDetectorCenter - outer_radius;

  float particleEnergy = particle->GetLorentzVector().E();

  return particleEnergy > distanceToDetector;
}