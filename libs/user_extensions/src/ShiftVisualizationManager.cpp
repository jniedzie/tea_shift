#include "ShiftVisualizationManager.hpp"

#include "ConfigManager.hpp"

using namespace std;

ShiftVisualizationManager::ShiftVisualizationManager(shared_ptr<ShiftDetector> detector_, double magField_)
    : detector(detector_), magField(magField_) {
  auto &config = ConfigManager::GetInstance();
  config.GetValue("doProjection", doProjection);
  config.GetValue("showAxes", showAxes);
  config.GetValue("backgroundColor", backgroundColor);
  config.GetValue("cmsColor", cmsColor);
  config.GetValue("shiftColor", shiftColor);

  rotation = detector->GetRotation();
  translation = detector->GetTranslation();

  SetupGeomManager();
  AddLHC();
  AddCMSDetector();
  AddSHIFT();

  geom->CloseGeometry();
  top->Draw("gl");
}

void ShiftVisualizationManager::SetupGeomManager() {
  geom = new TGeoManager("geom", "3D Geometry");
  matVacuum = new TGeoMaterial("Vacuum", 0, 0, 0);
  vacuum = new TGeoMedium("vacuum", 1, matVacuum);
  top = geom->MakeBox("top", vacuum, 200, 200, 200);
  geom->SetTopVolume(top);
}

pair<vector<TVector3>, vector<TVector3>> ShiftVisualizationManager::CalculateHelixPoints(TVector3 origin, TVector3 momentum, int charge) {
  vector<TVector3> helixPoints, linePoints;

  double detectorStartX = -detector->GetLength() / 2;
  double detectorStartY, detectorStartZ;
  double x, y, z, t;
  bool first = true;

  for (int i = 0; i < 100000; ++i) {
    t = i * 0.0001;  // Path length parameter
    x = origin.X() + t * momentum.X();
    y = origin.Y() + t * momentum.Y();
    z = origin.Z() + t * momentum.Z();

    if (first && x >= detectorStartX) {
      detectorStartY = y;
      detectorStartZ = z;
      first = false;
    }

    linePoints.push_back(TVector3(x, y, z));
    if (x > detectorStartX) break;
  }

  double pT = sqrt(momentum.Y() * momentum.Y() + momentum.Z() * momentum.Z());  // Transverse momentum in GeV/c
  double R = pT / (0.3 * magField);                                             // Radius of curvature in meters
  double slope = momentum.X() / pT;
  double inner_radius = detector->GetInnerRadius();
  double outer_radius = detector->GetOuterRadius();

  first = true;
  double correctionY, correctionZ;

  for (int i = 0; i < 100000; ++i) {
    t = i * 0.0001;                    // Path length parameter
    x = origin.X() + fabs(slope) * t;  // Longitudinal motion

    if (x < detectorStartX) continue;

    if (charge > 0) {
      y = origin.Y() + R * cos(t);  // Transverse motion in y
      z = origin.Z() + R * sin(t);  // Transverse motion in z
    } else {
      y = origin.Y() + R * sin(t);  // Transverse motion in y
      z = origin.Z() + R * cos(t);  // Transverse motion in z
    }

    if (first) {
      correctionY = y - detectorStartY;
      correctionZ = z - detectorStartZ;
      first = false;
    }

    y -= correctionY;
    z -= correctionZ;

    helixPoints.push_back(TVector3(x, y, z));
    if (x > fabs(detectorStartX)) break;
    double transverseDistance = sqrt(y * y + z * z);
    // if (transverseDistance < inner_radius || transverseDistance > outer_radius) break;
    if (transverseDistance > outer_radius) break;
  }

  return {helixPoints, linePoints};
}

vector<TVector3> ShiftVisualizationManager::CalculateDarkLine(TVector3 muonOrigin) {
  vector<TVector3> linePoints;

  double detectorStartX = -detector->GetLength() / 2;

  double dx = detector->GetTranslation().X() - muonOrigin.X();
  double dy = detector->GetTranslation().Y() - muonOrigin.Y();
  double dz = detector->GetTranslation().Z() - muonOrigin.Z();
  double dt = 0.3;

  double distance = std::sqrt(dx * dx + dy * dy + dz * dz);
  int num_steps = static_cast<int>(distance / dt) + 1;

  dx /= distance;
  dy /= distance;
  dz /= distance;

  double x, y, z, t;

  for (int i = 0; i <= num_steps; ++i) {
    t = i * dt;
    x = muonOrigin.X() + t * dx;
    y = muonOrigin.Y() + t * dy;
    z = muonOrigin.Z() + t * dz;

    linePoints.push_back(TVector3(x, y, z));
  }

  return linePoints;
}

void ShiftVisualizationManager::AddDarkLine(TVector3 origin) {
  auto linePoints = CalculateDarkLine(origin);

  auto line = new TEvePointSet();
  line->SetOwnIds(kTRUE);
  line->SetMarkerStyle(20);
  line->SetMarkerSize(0.2);
  line->SetMarkerColor(kBlack);

  for (size_t i = 0; i < linePoints.size(); ++i) {
    line->SetNextPoint(linePoints[i].X(), linePoints[i].Y(), linePoints[i].Z());
  }
  gEve->AddElement(line);
}

void ShiftVisualizationManager::AddHelixToVolume(TVector3 origin, TVector3 momentum, int charge) {
  auto [helixPoints, linePoints] = CalculateHelixPoints(origin, momentum, charge);

  auto helix = new TEvePointSet();
  helix->SetOwnIds(kTRUE);
  helix->SetMarkerStyle(20);
  helix->SetMarkerSize(0.2);
  helix->SetMarkerColor(kGreen);

  auto line = new TEvePointSet();
  line->SetOwnIds(kTRUE);
  line->SetMarkerStyle(20);
  line->SetMarkerSize(0.2);
  line->SetMarkerColor(kBlue);

  for (size_t i = 0; i < helixPoints.size(); ++i) {
    helix->SetNextPoint(helixPoints[i].X(), helixPoints[i].Y(), helixPoints[i].Z());
  }

  for (size_t i = 0; i < linePoints.size(); ++i) {
    line->SetNextPoint(linePoints[i].X(), linePoints[i].Y(), linePoints[i].Z());
  }
  gEve->AddElement(helix);
  gEve->AddElement(line);
}

void ShiftVisualizationManager::AddSHIFT() {
  auto shiftTube = new TGeoBBox(3, 1, 1);
  auto shiftVolume = new TGeoVolume("shiftVolume", shiftTube, vacuum);
  shiftVolume->SetLineColor(shiftColor);
  shiftVolume->SetFillColorAlpha(shiftColor, 1.0);
  auto rot = new TGeoRotation();
  Double_t matrix[9] = { rotation.XX(), rotation.XY(), rotation.XZ(), rotation.YX(), rotation.YY(), rotation.YZ(), rotation.ZX(), rotation.ZY(), rotation.ZZ() };
  rot->SetMatrix(matrix);
  top->AddNode(shiftVolume, 1, new TGeoCombiTrans(translation.X(), translation.Y(), translation.Z(), rot));
}

void ShiftVisualizationManager::AddLHC() {
  // auto lhcTorus = new TGeoTorus(4300, 0, 0.5, 265, 10);
  auto lhcTorus = new TGeoTorus(4300, 0, 0.5, 85, 10);
  auto lhcVolume = new TGeoVolume("lhcVolume", lhcTorus, vacuum);
  lhcVolume->SetLineColor(kGreen);
  lhcVolume->SetFillColorAlpha(kGreen, 1.0);
  auto rot = new TGeoRotation();
  
  top->AddNode(lhcVolume, 1, new TGeoCombiTrans(0, -4300, 0, rot));
}

void ShiftVisualizationManager::AddCMSDetector() {
  // Create CMS geometry
  auto detectorTube = detector->GetGeoTube();
  auto cmsVolume = new TGeoVolume("cmsVolume", detectorTube, vacuum);
  cmsVolume->SetLineColor(cmsColor);
  cmsVolume->SetFillColorAlpha(cmsColor, 0.8);  // Set fill color with transparency
  cmsVolume->SetTransparency(80);               // Set transparency (0-100, where 100 is fully transparent)
  auto rot = new TGeoRotation();
  rot->RotateY(90);  // Rotate 90 degrees around the Y-axis
  top->AddNode(cmsVolume, 1, new TGeoCombiTrans(0, 0, 0, rot));
}

void ShiftVisualizationManager::AddAxes() {
  // Add X-axis
  TEveLine *xAxis = new TEveLine();
  xAxis->SetPoint(0, 0, 0, 0);
  xAxis->SetPoint(1, 100, 0, 0);  // Extend the length as needed
  xAxis->SetLineColor(kRed);      // Color the X-axis red
  xAxis->SetLineWidth(2);
  gEve->AddElement(xAxis);

  // Add Y-axis
  TEveLine *yAxis = new TEveLine();
  yAxis->SetPoint(0, 0, 0, 0);
  yAxis->SetPoint(1, 0, 100, 0);  // Extend the length as needed
  yAxis->SetLineColor(kGreen);    // Color the Y-axis green
  yAxis->SetLineWidth(2);
  gEve->AddElement(yAxis);

  // Add Z-axis
  TEveLine *zAxis = new TEveLine();
  zAxis->SetPoint(0, 0, 0, 0);
  zAxis->SetPoint(1, 0, 0, 100);  // Extend the length as needed
  zAxis->SetLineColor(kBlue);     // Color the Z-axis blue
  zAxis->SetLineWidth(2);
  gEve->AddElement(zAxis);
}

void ShiftVisualizationManager::Visualize(set<shared_ptr<HepMCParticle>> muons) {
  // Start the event display
  TEveManager::Create();
  auto topNode = new TEveGeoTopNode(geom, geom->GetTopNode());
  gEve->AddGlobalElement(topNode);
  gEve->Redraw3D(kTRUE);

  bool first = true;

  for (auto muon : muons) {
    auto origin = muon->GetOrigin();
    auto momentum = muon->GetMomentum();
    int charge = muon->GetCharge();

    origin *= rotation;
    origin += translation;
    momentum *= rotation;

    info() << "Muon origin: " << origin.X() << " " << origin.Y() << " " << origin.Z() << endl;
    info() << "Muon momentum: " << momentum.X() << " " << momentum.Y() << " " << momentum.Z() << endl;

    AddHelixToVolume(origin, momentum, charge);

    if (first) {
      AddDarkLine(origin);
      first = false;
    }
  }

  if (showAxes) AddAxes();

  geom->SetTopVisible(kTRUE);

  TEveViewer *viewer = gEve->GetDefaultViewer();
  TGLViewer *glViewer = viewer->GetGLViewer();

  map<string, TGLViewer::ECameraType> cameraTypes = {

      {"kCameraPerspXOZ", TGLViewer::kCameraPerspXOZ},   {"kCameraPerspYOZ", TGLViewer::kCameraPerspYOZ},
      {"kCameraPerspXOY", TGLViewer::kCameraPerspXOY},   {"kCameraOrthoXOY", TGLViewer::kCameraOrthoXOY},

      {"kCameraOrthoXOZ", TGLViewer::kCameraOrthoXOZ},   {"kCameraOrthoZOY", TGLViewer::kCameraOrthoZOY},
      {"kCameraOrthoZOX", TGLViewer::kCameraOrthoZOX},   {"kCameraOrthoXnOY", TGLViewer::kCameraOrthoXnOY},

      {"kCameraOrthoXnOZ", TGLViewer::kCameraOrthoXnOZ}, {"kCameraOrthoZnOY", TGLViewer::kCameraOrthoZnOY},
      {"kCameraOrthoZnOX", TGLViewer::kCameraOrthoZnOX},

  };

  if (doProjection != "") {
    glViewer->SetCurrentCamera(cameraTypes.at(doProjection));
  }
  
  glViewer->SetClearColor(backgroundColor);
  
  // glViewer->SetLOD(2);
  gGeoManager->SetNsegments(100);

  gEve->Redraw3D(kTRUE);
}