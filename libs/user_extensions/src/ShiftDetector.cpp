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
    outer_radius = params.at("radius");
    total_length = params.at("length");
    x = params.at("x");
    y = params.at("y");
    z = params.at("z");
    
    double maxEta = params.at("maxEta");
    double theta_inner = 2 * std::atan(std::exp(-maxEta));
    inner_radius = total_length / 2.0 * tan(theta_inner);

    float lhc_radius = 4300;  // [m]
    rotation.SetToIdentity();

    if (y < 0) {
      forcedLHCring = true;
      
      float y_1 = sqrt(pow(lhc_radius, 2) - pow(x, 2)) + lhc_radius;
      float y_2 = -sqrt(pow(lhc_radius, 2) - pow(x, 2)) + lhc_radius;
      y = min(y_1, y_2);

      double theta = TMath::Pi() + TMath::ATan2(-x, y-lhc_radius);
      info() << "Theta: " << theta << endl;
      rotation.RotateZ(theta);
    }

    // old implementation with a bug
    // double theta = TMath::ATan2(y, x);
    // rotation.RotateY(theta);

    TVector3 detectorCenter(x, y, z);

    // old implementation with a bug
    // detectorCenter *= rotation;

    translation = -detectorCenter;
  }
}

void ShiftDetector::Print() {
  if(isLHCb){
    info() << "\n\033[1;36m"
           << "╔════════════════════════════════════════════╗\n"
           << "║              LHCb Detector Info           ║\n"
           << "╠══════════════════════════╤════════════════╣\n"
           << "║ Parameter                │ Value          ║\n"
           << "╠══════════════════════════╪════════════════╣\n"
           << "║ minLength                │ " << setw(14) << minLength << " ║\n"
           << "║ maxLength                │ " << setw(14) << maxLength << " ║\n"
           << "║ minEta                   │ " << setw(14) << minEta << " ║\n"
           << "║ maxEta                   │ " << setw(14) << maxEta << " ║\n"
           << "╚══════════════════════════╧════════════════╝\033[0m\n\n";
    return;
  }

  float distance = sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2));
  float fullArea = 4 * TMath::Pi() * distance * distance;
  float detectorArea = TMath::Pi() * outer_radius * outer_radius;
  float angularCoverage = detectorArea / fullArea;

  info() << "\n\033[1;36m"
         << "╔════════════════════════════════════════════╗\n"
         << "║            Detector Information            ║\n"
         << "╠══════════════════════════╤═════════════════╣\n"
         << "║ Parameter                │ Value           ║\n"
         << "╠══════════════════════════╪═════════════════╣\n"
         << "║ Position (x, y, z) [m]   │ " << setw(4) << "(" << translation.X() << ", "
         << translation.Y() << ", " << translation.Z() << ")" << setw(4) << " ║\n"
         << "║ Rotation (angle) [rad]   │ " << setw(14) << rotation.ThetaZ() << " ║\n"
         
         << "║ Total distance [m]       │ " << setw(14) << distance << "  ║\n"
         << "║ Outer radius [m]         │ " << setw(14) << outer_radius << "  ║\n"
         << "║ Inner radius [m]         │ " << setw(14) << inner_radius << "  ║\n"
         << "║ Total length [m]         │ " << setw(14) << total_length << "  ║\n"
         
         << "║ Angular coverage         │ " << setw(14) << angularCoverage << "  ║\n"
         << "║ On LHC ring              │ " << setw(14) << (forcedLHCring ? "yes" : "no") << "  ║\n"
         << "╚══════════════════════════╧═════════════════╝\033[0m\n\n";
}

bool ShiftDetector::DoesParticleGoThrough(const shared_ptr<HepMCParticle> &particle) {
  if(isLHCb){
    return IsWithinLHCbAcceptance(particle);
  }

  // convert mm to m. x is our y, y is our z, z is our x
  TVector3 particleOrigin(particle->GetZ() / 1e3, particle->GetX() / 1e3, particle->GetY() / 1e3);

  auto fourVector = particle->GetLorentzVector();
  float eta = fourVector.Eta();
  float phi = fourVector.Phi();
  TVector3 direction(std::sinh(eta), std::cos(phi), std::sin(phi));

  // Move and rotate the particleOrigin and direction to the detector's frame (x: along the beam, y: along LHC's radius)
  particleOrigin *= rotation;
  particleOrigin += translation;
  direction *= rotation;

  if (direction.Mag() == 0) {
    error() << "Particle direction is zero, cannot determine if it goes through the detector." << endl;
    return false;
  }

  TVector3 unitDirection = direction.Unit();

  // If the particle is produced outside the detector, check if it's moving towards the detector:

  // In the radial direction from the cylinder axis (assume axis along X)
  TVector3 axisDir(1, 0, 0);  // Assuming cylinder axis is along X
  TVector3 radialVector = particleOrigin - axisDir * (particleOrigin * axisDir);
  TVector3 radialDir = unitDirection - axisDir * (unitDirection * axisDir);
  if (radialVector.Mag() > outer_radius) {
    if (radialVector.Dot(radialDir) > 0) {
      return false;  // Moving away from the cylinder radially
    }
  }

  // In the z-direction
  if ((particleOrigin.X() > total_length / 2 && unitDirection.X() > 0) || (particleOrigin.X() < -total_length / 2 && unitDirection.X() < 0)) {
    return false;  // Moving away from the cylinder along the z-axis
  }

  // Endcap intersection checks
  double x1 = -total_length / 2 - particleOrigin.X();
  double x2 = total_length / 2 - particleOrigin.X();
  double t1 = x1 / unitDirection.X();
  double t2 = x2 / unitDirection.X();

  for (double t : {t1, t2}) {
    if (t < 0) {  // Only consider t >= 0 for valid intersection direction
      continue;
    }
    TVector3 intersectionPoint = particleOrigin + t * unitDirection;
    double radialDistance = TMath::Sqrt(intersectionPoint.Y() * intersectionPoint.Y() + intersectionPoint.Z() * intersectionPoint.Z());
    if (radialDistance >= inner_radius && radialDistance <= outer_radius) {
      return true;
    }
  }

  // Outer cylinder intersection check
  double a = unitDirection.Y() * unitDirection.Y() + unitDirection.Z() * unitDirection.Z();
  double b = 2 * (particleOrigin.Y() * unitDirection.Y() + particleOrigin.Z() * unitDirection.Z());
  double c = particleOrigin.Y() * particleOrigin.Y() + particleOrigin.Z() * particleOrigin.Z() - outer_radius * outer_radius;
  double discriminant = b * b - 4 * a * c;

  if (discriminant >= 0) {
    double t3 = (-b - TMath::Sqrt(discriminant)) / (2 * a);
    double t4 = (-b + TMath::Sqrt(discriminant)) / (2 * a);

    for (double t : {t3, t4}) {
      if (t < 0) {
        continue;
      }
      TVector3 intersectionPoint = particleOrigin + t * unitDirection;
      if (intersectionPoint.X() >= -total_length / 2 && intersectionPoint.X() <= total_length / 2) {
        return true;
      }
    }
  }

  // Inner cylinder intersection check
  c = particleOrigin.Y() * particleOrigin.Y() + particleOrigin.Z() * particleOrigin.Z() - inner_radius * inner_radius;
  discriminant = b * b - 4 * a * c;

  if (discriminant >= 0) {
    double t3 = (-b - TMath::Sqrt(discriminant)) / (2 * a);
    double t4 = (-b + TMath::Sqrt(discriminant)) / (2 * a);

    for (double t : {t3, t4}) {
      if (t < 0) {
        continue;
      }
      TVector3 intersectionPoint = particleOrigin + t * unitDirection;
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

bool ShiftDetector::DoesParticleGoThroughRock(const shared_ptr<HepMCParticle> &particle, const std::shared_ptr<PhysicsObjects>& allParticles) {
  if(isLHCb){
    return true;
  }
  if (x == 0 && y == 0 && z == 0) {
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

  bool muonGoesThrough = particleEnergy > criticalEnergy;
  if(!muonGoesThrough){
    return false;
  }

  // check if the mother particle is stopped before it decays
  auto mother = particle->GetMother(allParticles);
  int motherPid = mother->GetPid();

  // check if mother is a dark hadron or a dark photon
  if (fabs(motherPid) == 4900111 || fabs(motherPid) == 4900113 || fabs(motherPid) == 32) {
    // if so, it doesn't interact with the rock, so it's fine
    return true;
  }

  // in all other cases, it's either prompt, or it's a hadron. We assume the same stopping power for all hadrons
  double motherPathLength = sqrt(xProd * xProd + yProd * yProd + zProd * zProd);
  
  double distanceToRock = 10; // [m]
  double maxDistanceInRock = 1; // [m]

  // the mother can only survive if it decays before it reaches the rock or at most 1m inside the rock
  return motherPathLength < distanceToRock + maxDistanceInRock;
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
