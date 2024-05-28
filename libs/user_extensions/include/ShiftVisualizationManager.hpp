#ifndef ShiftVisualizationManager_hpp
#define ShiftVisualizationManager_hpp

#include "HepMCParticle.hpp"
#include "Logger.hpp"
#include "Helpers.hpp"
#include "ShiftDetector.hpp"

class ShiftVisualizationManager {
 public:
  ShiftVisualizationManager(std::shared_ptr<ShiftDetector> detector_, double magField_);
  ~ShiftVisualizationManager() {}

  void Visualize(std::set<std::shared_ptr<HepMCParticle>> muons);

  std::pair<std::vector<TVector3>, std::vector<TVector3>> CalculateHelixPoints(TVector3 origin, TVector3 momentum, int charge);
  void AddHelixToVolume(TVector3 origin, TVector3 momentum, int charge);

 private:
  std::shared_ptr<ShiftDetector> detector;
  double magField;

  TGeoManager *geom;
  TGeoVolume *top;
  TGeoMaterial *matVacuum;
  TGeoMedium *vacuum;

  TRotation rotation;
  TVector3 translation;

  void SetupGeomManager();
  void AddCMSDetector();
  void AddSHIFT();
  void AddAxes();
};

#endif /* ShiftVisualizationManager_hpp */