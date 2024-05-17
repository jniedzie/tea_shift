#include "ShiftDetector.hpp"

using namespace std;

ShiftDetector::ShiftDetector(const std::map<std::string, float> &params, bool isLHCb_) :
isLHCb(isLHCb_){
  if(isLHCb){
    minLength = params.at("minLength");
    maxLength = params.at("maxLength");
    minEta = params.at("minEta");
    maxEta = params.at("maxEta");
    maxDistance = minLength + (maxLength - minLength)/2;
  }
  else{
    x = params.at("x");
    y = params.at("y");
    z = params.at("z");
    outer_radius = params.at("radius");
    total_length = params.at("length");
    double maxEta = params.at("maxEta");

    double theta_inner = 2 * std::atan(std::exp(-2.4));
    inner_radius = total_length / 2.0 * tan(theta_inner);

    if (y < 0) {
      forcedLHCring = true;
      float lhc_radius = 4300;  // [m]
      float y_1 = sqrt(pow(lhc_radius, 2) - pow(x, 2)) + lhc_radius;
      float y_2 = -sqrt(pow(lhc_radius, 2) - pow(x, 2)) + lhc_radius;
      y = min(y_1, y_2);
    }

    double theta = TMath::ATan2(y, x);
    rotation.RotateY(theta);

    TVector3 detectorCenter(x, y, z);

    auto newCenter = detectorCenter;
    newCenter *= rotation;
    translation = -newCenter;
  }
}

void ShiftDetector::Print() {
  if(isLHCb){
    info() << "\n\n--------------------------------------------------" << endl;
    info() << "Detector at LHCb" << endl;
    info() << "Length: " << minLength << " < L < " << maxLength << endl;
    info() << "Eta: " << minEta << " < eta < " << maxEta << endl;
    info() << "--------------------------------------------------\n\n" << endl;
    return;
  }

  info() << "\n\n--------------------------------------------------" << endl;
  info() << "Detector at: (" << x << ", " << y << ", " << z << ") " << endl;
  info() << "Total distance: " << sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2)) << endl;
  info() << "Outer radius: " << outer_radius << "\tinner radius: " <<inner_radius << "\tlength: " << total_length << endl;
  // calculate the fraction of the solid angle the detector covers
  float distance = sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2));
  float fullArea = 4 * TMath::Pi() * distance * distance;
  float detectorArea = TMath::Pi() * outer_radius * outer_radius;
  info() << "Angular coverage: " << detectorArea / fullArea << endl;
  info() << "Forced to be on the LHC ring: " << (forcedLHCring ? "yes" : "no") << endl;
  info() << "--------------------------------------------------\n\n" << endl;
}

bool ShiftDetector::DoesParticleGoThrough(const shared_ptr<HepMCParticle> &particle) {
  if(isLHCb){
    return IsWithinLHCbAcceptance(particle);
  }

  // convert mm to m. x is our y, y is our z, z is our x
  TVector3 origin(particle->GetZ() / 1e3, particle->GetX() / 1e3, particle->GetY() / 1e3);

  auto fourVector = particle->GetLorentzVector();
  float eta = fourVector.Eta();
  float phi = fourVector.Phi();
  TVector3 direction(std::sinh(eta), std::cos(phi), std::sin(phi));

  // Move and rotate the origin and direction to the detector's frame (x: along the beam, y: along LHC's radius)
  origin *= rotation;
  origin += translation;
  direction *= rotation;

  if (direction.Mag() == 0) {
    return false;
  }

  TVector3 unitDirection = direction.Unit();

  // If the particle is produced outside the detector, check if it's moving towards the detector:

  // In the transverse plane
  TVector3 radialOrigin(origin.Y(), origin.Z(), 0);
  TVector3 radialDirection(unitDirection.Y(), unitDirection.Z(), 0);
  if (radialOrigin.Mag() > outer_radius) {
    if (radialOrigin.Dot(radialDirection) > 0) {
      return false;  // Moving away from the cylinder radially
    }
  }

  // In the z-direction
  if ((origin.X() > total_length / 2 && unitDirection.X() > 0) || (origin.X() < -total_length / 2 && unitDirection.X() < 0)) {
    return false;  // Moving away from the cylinder along the z-axis
  }

  // Endcap intersection checks
  double x1 = -total_length / 2 - origin.X();
  double x2 = total_length / 2 - origin.X();
  double t1 = x1 / unitDirection.X();
  double t2 = x2 / unitDirection.X();

  for (double t : {t1, t2}) {
    if (t < 0) {  // Only consider t >= 0 for valid intersection direction
      continue;
    }
    TVector3 intersectionPoint = origin + t * unitDirection;
    double radialDistance = TMath::Sqrt(intersectionPoint.Y() * intersectionPoint.Y() + intersectionPoint.Z() * intersectionPoint.Z());
    if (radialDistance >= inner_radius && radialDistance <= outer_radius) {
      return true;
    }
  }

  // Outer cylinder intersection check
  double a = unitDirection.Y() * unitDirection.Y() + unitDirection.Z() * unitDirection.Z();
  double b = 2 * (origin.Y() * unitDirection.Y() + origin.Z() * unitDirection.Z());
  double c = origin.Y() * origin.Y() + origin.Z() * origin.Z() - outer_radius * outer_radius;
  double discriminant = b * b - 4 * a * c;

  if (discriminant >= 0) {
    double t3 = (-b - TMath::Sqrt(discriminant)) / (2 * a);
    double t4 = (-b + TMath::Sqrt(discriminant)) / (2 * a);

    for (double t : {t3, t4}) {
      if (t < 0) {
        continue;
      }
      TVector3 intersectionPoint = origin + t * unitDirection;
      if (intersectionPoint.X() >= -total_length / 2 && intersectionPoint.X() <= total_length / 2) {
        return true;
      }
    }
  }

  // Inner cylinder intersection check
  c = origin.Y() * origin.Y() + origin.Z() * origin.Z() - inner_radius * inner_radius;
  discriminant = b * b - 4 * a * c;

  if (discriminant >= 0) {
    double t3 = (-b - TMath::Sqrt(discriminant)) / (2 * a);
    double t4 = (-b + TMath::Sqrt(discriminant)) / (2 * a);

    for (double t : {t3, t4}) {
      if (t < 0) {
        continue;
      }
      TVector3 intersectionPoint = origin + t * unitDirection;
      if (intersectionPoint.X() >= -total_length / 2 && intersectionPoint.X() <= total_length / 2) {
        return true;
      }
    }
  }

  return false;
}

bool ShiftDetector::IsProductionVertexBeforeTheEnd(const shared_ptr<HepMCParticle> &particle, float maxDistanceInsideDetector) {
  if(isLHCb){
    return true;
  }
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
  if(isLHCb){
    return true;
  }
  // calculate the distance the particle has to travel from production vertex to the edge of the detector
  // convert mm to m. x is our y, y is our z, z is our x
  float xProd = particle->GetZ() / 1e3;
  float yProd = particle->GetX() / 1e3;
  float zProd = particle->GetY() / 1e3;

  float distanceToDetectorCenter = sqrt(pow(xProd - x, 2) + pow(yProd - y, 2) + pow(zProd - z, 2));
  float distanceToDetector = distanceToDetectorCenter - outer_radius;

  float particleEnergy = particle->GetLorentzVector().E();

  float criticalEnergy = 0.5 * distanceToDetector + 1;

  return particleEnergy > criticalEnergy;
}

bool ShiftDetector::IsWithinLHCbAcceptance(const std::shared_ptr<HepMCParticle> &particle) {


  // convert mm to m. x is our y, y is our z, z is our x
  float xProd = particle->GetZ() / 1e3;
  float yProd = particle->GetX() / 1e3;
  float zProd = particle->GetY() / 1e3;

  float particleDistance = sqrt(pow(xProd, 2) + pow(yProd, 2) + pow(zProd, 2));

  if (particleDistance > maxDistance) {
    return false;
  }

  float eta = fabs(particle->GetLorentzVector().Eta());
  if (eta > maxEta || eta < minEta) {
    return false;
  }

  return true;
}
