#include "ConfigManager.hpp"
#include "CutFlowManager.hpp"
#include "EventReader.hpp"
#include "ExtensionsHelpers.hpp"
#include "HistogramsFiller.hpp"
#include "HistogramsHandler.hpp"
#include "ShiftDetector.hpp"
#include "ShiftHistogramsFiller.hpp"
#include "ShiftObjectsManager.hpp"

using namespace std;

void CheckArgs(int argc, char **argv) {
  if (argc != 2 && argc != 5) {
    fatal() << "Usage: " << argv[0] << " config_path" << endl;
    fatal() << "or" << endl;
    fatal() << argv[0] << " config_path input_path trees_output_path histograms_output_path" << endl;
    exit(1);
  }
}

std::vector<std::tuple<double, double, double>> CalculateHelixPoints(Double_t x0, Double_t y0, Double_t z0, Double_t px, Double_t py,
                                                                     Double_t pz, Double_t charge, Double_t B, Double_t length,
                                                                     Int_t nPoints) {
  std::vector<std::tuple<double, double, double>> points;
  Double_t pt = sqrt(px * px + py * py);      // Transverse momentum
  Double_t omega = charge * B / pt;           // Angular frequency of the helix (omega = qB/pT)
  Double_t period = 2 * TMath::Pi() / omega;  // Period of one full circle in the helix
  Double_t dz = length / nPoints;

  for (int i = 0; i <= nPoints; ++i) {
    Double_t t = i * dz / pz;  // Time parameter
    Double_t x = x0 + px * t;
    Double_t y = y0 + (pt / (charge * B)) * sin(omega * t);
    Double_t z = z0 + (pt / (charge * B)) * (1 - cos(omega * t));
    points.push_back({x, y, z});
  }
  return points;
}

void AddHelixToVolume(TGeoVolume *top, Double_t x0, Double_t y0, Double_t z0, Double_t px, Double_t py, Double_t pz, Double_t charge,
                      Double_t B, Double_t length, Int_t nPoints) {
  auto points = CalculateHelixPoints(x0, y0, z0, px, py, pz, charge, B, length, nPoints);

  auto vacuum = top->GetMedium();
  Double_t segmentLength = length / nPoints;

  for (size_t i = 0; i < points.size() - 1; ++i) {
    Double_t x1 = get<0>(points[i]);
    Double_t y1 = get<1>(points[i]);
    Double_t z1 = get<2>(points[i]);
    Double_t x2 = get<0>(points[i + 1]);
    Double_t y2 = get<1>(points[i + 1]);
    Double_t z2 = get<2>(points[i + 1]);

    auto segment = new TGeoTube(0, 0.1, segmentLength / 2);  // small radius for the helix path
    auto segmentVol = new TGeoVolume("segment", segment, vacuum);
    segmentVol->SetLineColor(kRed);

    Double_t dx = x2 - x1;
    Double_t dy = y2 - y1;
    Double_t dz = z2 - z1;
    Double_t lengthSegment = sqrt(dx * dx + dy * dy + dz * dz);

    info() << "x1: " << x1 << ", y1: " << y1 << ", z1: " << z1 << endl;
    info() << "x2: " << x2 << ", y2: " << y2 << ", z2: " << z2 << endl;

    auto rotation = new TGeoRotation();
    rotation->RotateZ(TMath::ATan2(dy, dx) * TMath::RadToDeg());
    rotation->RotateY(TMath::ACos(dz / lengthSegment) * TMath::RadToDeg());
    auto transform = new TGeoCombiTrans((x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2, rotation);
    top->AddNode(segmentVol, i, transform);
  }
}

void DrawCylinderWithHole(shared_ptr<HepMCParticle> muon1) {
  // Define parameters for the cylinder
  Double_t outerRadius = 7.5;
  Double_t innerRadius = 2.01236;
  Double_t length = 22;

  // Create a new TGeoManager
  auto geom = new TGeoManager("geom", "3D Geometry");
  // geom->SetTopVisible(kTRUE); // Ensure top volume is visible
  // geom->GetTopVolume()->SetVisibility(kTRUE); // Ensure the top volume is visible
  // geom->GetTopNode()->SetVisContainers(kTRUE); // Make sure all contained volumes are visible
  // geom->SetRange(-100, -100, -100, 100, 100, 100); // Set the range to zoom out

  // Create materials and media
  TGeoMaterial *matVacuum = new TGeoMaterial("Vacuum", 0, 0, 0);
  TGeoMedium *vacuum = new TGeoMedium("vacuum", 1, matVacuum);

  // Create top volume
  TGeoVolume *top = geom->MakeBox("top", vacuum, 50, 50, 50);
  geom->SetTopVolume(top);

  // Create a cylinder with an inner hole using TGeoTube
  TGeoTube *tube = new TGeoTube(innerRadius, outerRadius, length / 2);
  TGeoVolume *cylinder = new TGeoVolume("cylinder", tube, vacuum);

  // Create a rotation matrix to rotate the cylinder along the x-axis
  TGeoRotation *rot = new TGeoRotation();
  rot->RotateY(90);  // Rotate 90 degrees around the Y-axis

  // Set the transparency and color of the cylinder
  cylinder->SetLineColor(kBlue);
  cylinder->SetFillColorAlpha(kBlue, 0.5);  // Set fill color with transparency
  cylinder->SetTransparency(50);            // Set transparency (0-100, where 100 is fully transparent)

  // Add the cylinder to the top volume with the rotation
  top->AddNode(cylinder, 1, new TGeoCombiTrans(0, 0, 0, rot));

  // Close the geometry
  geom->CloseGeometry();

  // Create a canvas to draw on
  TCanvas *c = new TCanvas("c", "Cylinder with Hole", 800, 600);
  TView *view = TView::CreateView(1);
  view->SetRange(-1000, -1000, -100, 100, 100, 100);

  // Draw the geometry with solid fill and transparency
  top->Draw("gl");
  // c->Update();

  // mm -> m
  // double z0 = muon1->GetX() / 1e3; 
  // double x0 = muon1->GetY() / 1e3;
  // double y0 = muon1->GetZ() / 1e3;

  double z0 = 0;
  double x0 = 0;
  double y0 = 0;

  double px = muon1->GetPx() / 1e3;
  double py = muon1->GetPy() / 1e3;
  double pz = muon1->GetPz() / 1e3;
  int charge = muon1->GetCharge();
  double B = 1.0;
  AddHelixToVolume(top, x0, y0, z0, px, py, pz, charge, B, 20000, 200);

  c->Update();
  c->SaveAs("../plots/visualization.pdf");
}

int main(int argc, char **argv) {
  CheckArgs(argc, argv);

  ConfigManager::Initialize(argv[1]);
  auto &config = ConfigManager::GetInstance();

  if (argc == 5) {
    config.SetInputPath(argv[2]);
    config.SetTreesOutputPath(argv[3]);
    config.SetHistogramsOutputPath(argv[4]);
  }

  /*
    auto args = make_unique<ArgsManager>(argc, argv);

  // check if optional value "config" is present
  if (!args->GetString("config").has_value()) {
    fatal() << "No config file provided" << endl;
    exit(1);
  }

  ConfigManager::Initialize(args->GetString("config").value());
  auto &config = ConfigManager::GetInstance();

  if (args->GetString("input_path").has_value()) {
    config.SetInputPath(args->GetString("input_path").value());
  }

  if (args->GetString("output_trees_path").has_value()) {
    config.SetTreesOutputPath(args->GetString("output_trees_path").value());
  }

  if (args->GetString("output_hists_path").has_value()) {
    config.SetHistogramsOutputPath(args->GetString("output_hists_path").value());
  }

  if (args->GetInt("some_number").has_value()){
    info() << "Some number: " << args->GetInt("some_number").value() << endl;
  }

  if (args->GetString("redirector").has_value()){
    info() << "Redirector: " << args->GetString("redirector").value() << endl;
  }
  */

  auto eventReader = make_shared<EventReader>();
  auto eventWriter = make_shared<EventWriter>(eventReader);
  auto histogramsHandler = make_shared<HistogramsHandler>();
  auto histogramsFiller = make_unique<HistogramsFiller>(histogramsHandler);
  auto shiftHistogramsFiller = make_unique<ShiftHistogramsFiller>(histogramsHandler);
  auto shiftObjectsManager = make_unique<ShiftObjectsManager>();
  auto cutFlowManager = make_shared<CutFlowManager>(eventReader, eventWriter);

  map<string, float> detectorParams;
  config.GetMap("detectorParams", detectorParams);

  string variant;
  config.GetValue("variant", variant);

  cutFlowManager->RegisterCut("initial");
  cutFlowManager->RegisterCut("hasMuons");
  cutFlowManager->RegisterCut("triggerAndReco");
  cutFlowManager->RegisterCut("intersectingDetector");
  cutFlowManager->RegisterCut("beforeDetector");
  cutFlowManager->RegisterCut("throughRock");
  cutFlowManager->RegisterCut("massCut");

  auto detector = make_shared<ShiftDetector>(detectorParams, variant == "lhcb");
  detector->Print();

  shared_ptr<HepMCParticle> muon1;
  shared_ptr<HepMCParticle> muon2;

  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);

    cutFlowManager->UpdateCutFlow("initial");
    auto nMuons = make_shared<map<string, int>>();
    nMuons->insert({"1_hasMuons", 0});
    nMuons->insert({"2_triggerAndReco", 0});
    nMuons->insert({"3_intersectingDetector", 0});
    nMuons->insert({"4_beforeDetector", 0});
    nMuons->insert({"5_throughRock", 0});

    shiftObjectsManager->InsertIndexedParticles(event);

    shiftObjectsManager->InsertGoodZprimesCollection(event);
    shiftObjectsManager->InsertGoodDarkHadronsCollection(event);
    shiftObjectsManager->InsertGoodMuonsCollection(event);
    shiftObjectsManager->InsertMuonsHittingDetectorCollection(event, detectorParams, variant, nMuons);
    shiftObjectsManager->InsertGoodDarkPhotonsCollection(event);

    shiftHistogramsFiller->Fill(event, true);

    bool passes = true;
    for (auto &[key, value] : *nMuons) {
      if (value < 2) {
        passes = false;
        break;
      }
      // remove everything before underscore:
      string name = key.substr(key.find("_") + 1);
      cutFlowManager->UpdateCutFlow(name);
    }
    if (!passes) continue;

    // check that at least one combination of muons passes the mass cut
    bool passesMassCut = false;

    auto muons = event->GetCollection("muonsInDetector");
    for (int i = 0; i < muons->size(); i++) {
      auto physicsObject = muons->at(i);
      auto hepMCParticle = asHepMCParticle(physicsObject);
      auto fourVector = hepMCParticle->GetLorentzVector();
      for (int j = i + 1; j < muons->size(); j++) {
        auto physicsObject2 = muons->at(j);
        auto hepMCParticle2 = asHepMCParticle(physicsObject2);
        auto fourVector2 = hepMCParticle2->GetLorentzVector();
        auto dimuon = fourVector + fourVector2;
        if (dimuon.M() > 11.0) {
          passesMassCut = true;
          muon1 = hepMCParticle;
          muon2 = hepMCParticle2;
          break;
        }
      }
      if (passesMassCut) break;
    }
    if (!passesMassCut) continue;
    cutFlowManager->UpdateCutFlow("massCut");

    // if making visualization, break once the first passing event is found
    break;

    shiftHistogramsFiller->Fill(event, false);
    eventWriter->AddCurrentEvent("Events");
  }

  DrawCylinderWithHole(muon1);

  histogramsFiller->FillCutFlow(cutFlowManager);
  histogramsHandler->SaveHistograms();

  cutFlowManager->SaveCutFlow();
  cutFlowManager->Print();

  eventWriter->Save();

  auto &logger = Logger::GetInstance();
  logger.Print();

  return 0;
}