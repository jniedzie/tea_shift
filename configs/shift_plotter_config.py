import ROOT
from Sample import Sample, SampleType
from Legend import Legend
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType

from shift_paths import crossSections, base_path, variant, colliderMode, luminosity

variant = "cms"
colliderMode = True

# variant = "shift160m"
# colliderMode = False

output_path = f"../plots/{variant}/"

backgrounds_legend_x = 0.60
signals_legend_x = 0.20

legend_max_y = 0.89

legend_width = 0.15
legend_height = 0.04

signal_ref_cross_section = 20e-5

samples = [
    Sample(
        name="pythia_qcd",
        file_path=f"{base_path}/pythia{'Collider' if colliderMode else ''}_qcd/merged_{variant}_histograms.root",
        type=SampleType.background,
        cross_sections=crossSections,
        
        fill_color=ROOT.kGray,
        fill_alpha=1.0,
        marker_size=0.0,
        
        legend_description="QCD",
        custom_legend=Legend(backgrounds_legend_x, legend_max_y-legend_height, backgrounds_legend_x+legend_width, legend_max_y, "FL"),
    ),
    Sample(
        name="pythia_dy",
        file_path=f"{base_path}/pythia{'Collider' if colliderMode else ''}_dy/merged_{variant}_histograms.root",
        type=SampleType.background,
        cross_sections=crossSections,

        fill_color=ROOT.kGray+1,
        fill_alpha=1.0,
        marker_size=0.0,
        
        legend_description="DY",
        custom_legend=Legend(backgrounds_legend_x, legend_max_y-2*legend_height, backgrounds_legend_x+legend_width, legend_max_y-legend_height, "FL"),
    ),
]

# custom_stacks_order = ["pythia_dy", "pythia_qcd"]
custom_stacks_order = ["pythia_qcd", "pythia_dy"]

custom_titles = {
    "pythia_mDarkPhoton-5_ctau-1e1": "DP: m_{A'} = 5 GeV, c#tau = 10^{1} m",
    "pythia_mDarkPhoton-30_ctau-1e1": "DP: m_{A'} = 30 GeV, c#tau = 10^{1} m",
    "pythia_mDarkPhoton-30_ctau-1em3": "DP: m_{A'} = 30 GeV, c#tau = 10^{-3} m",
    "pythia_mDarkPhoton-30_ctau-1e3": "DP: m_{A'} = 30 GeV, c#tau = 10^{3} m",
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em1": "HV: m_{D} = 5 GeV, c#tau = 10^{-1} m",
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1em1": "HV: m_{D} = 20 GeV, c#tau = 10^{-1} m",
    "pythia_mZprime-60_mDH-20_mDQ-1_tau-1em1": "HV: m_{D} = 20 GeV, c#tau = 10^{-1} m",
}

def addSignalSample(name, color, legend_y, custom_variant=variant):
    
    file_name = name.replace("pythia_", "pythiaCollider_") if colliderMode else name
    
    if name in custom_titles:
        title = custom_titles[name]
    else:
        title = name.replace("pythia_mDarkPhoton-", "m_{A'} = ")
        title = name.replace("pythia_mZprime-100_mDH-20_mDQ-1_", "")
        title = name.replace("pythia_mZprime-100_mDH-90_mDQ-1_", "")
        title = name.replace("pythia_mZprime-100_mDH-40_mDQ-1_", "")
        title = name.replace("pythia_mZprime-100_mDH-20_mDQ-10_", "")
        title = name.replace("pythia_mZprime-60_mDH-5_mDQ-1_", "")
        title = title.replace("ctau-", "c#tau=")
        title = title.replace("tau-", "c#tau=")
        title = title.replace("1em", "10^{-")
        title = title.replace("1e", "10^{")
        title += "} [m]"
    
    if custom_variant != variant:
        title += f" ({custom_variant})"
    
    samples.append(Sample(
        name=name,
        file_path=f"{base_path}/{file_name}/merged_{custom_variant}_histograms.root",
        type=SampleType.signal,
        cross_section=signal_ref_cross_section,
        line_alpha=1,
        line_style=1,
        fill_alpha=0,
        marker_size=0,
        line_color=color,
        legend_description=title,
        custom_legend=Legend(signals_legend_x, legend_y, signals_legend_x+legend_width, legend_y+legend_height, "L"),
    )
    )
    print(f"{signals_legend_x}, {legend_y}, {signals_legend_x+legend_width}, {legend_y+legend_height}")
    
    custom_stacks_order.append(name)

addSignalSample("pythia_mDarkPhoton-5_ctau-1e1", ROOT.kViolet, legend_max_y-legend_height)
addSignalSample("pythia_mDarkPhoton-30_ctau-1e1", ROOT.kBlue, legend_max_y-2*legend_height)
addSignalSample("pythia_mDarkPhoton-30_ctau-1em3", ROOT.kCyan, legend_max_y-3*legend_height)
addSignalSample("pythia_mDarkPhoton-30_ctau-1e3", ROOT.kGreen, legend_max_y-4*legend_height)
addSignalSample("pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em1", ROOT.kOrange, legend_max_y-5*legend_height)
addSignalSample("pythia_mZprime-60_mDH-20_mDQ-1_ctau-1em1", ROOT.kRed, legend_max_y-6*legend_height)
# addSignalSample("pythia_mZprime-60_mDH-20_mDQ-1_tau-1em1", ROOT.kOrange+1, legend_max_y-6*legend_height)

# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3", ROOT.kRed, legend_max_y-7*legend_height)
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e5", ROOT.kMagenta, legend_max_y-8*legend_height)

y_label = "Events"

histograms = (

    Histogram("cutFlow", "", False, True, NormalizationType.to_lumi, 1, 0, 7, 1e-5, 1e10, "Selection", "#sum genWeight", "_"+variant),

    Histogram("GoodInitialMuons_energy", "", False, True, NormalizationType.to_lumi, 2,   30, 4000, 1, 1e12, "E^{#mu} [GeV]", "Entries", "_"+variant),
    Histogram("GoodInitialMuons_pt", "", False, True, NormalizationType.to_lumi, 1,   0, 100, 10, 1e12, "p_{T}^{#mu} [GeV]", "Entries", "_"+variant),
    Histogram("GoodInitialMuons_eta", "", False, True, NormalizationType.to_lumi, 1,   -10, 10, 1e0, 1e12, "#eta^{#mu}", "Entries", "_"+variant),
    Histogram("GoodInitialMuons_d3d", "", True, True, NormalizationType.to_lumi, 2,   1e-7, 1e7, 1e0, 1e12, "d_{3D}^{#mu} [m]", "Entries", "_"+variant),
    Histogram("GoodInitialMuons_properCtau", "", True, True, NormalizationType.to_lumi, 1,   1e-7, 1e7, 5e-1, 1e10, "c#tau^{#mu} [m]", "Entries", "_"+variant),
    Histogram("GoodInitialMuons_boost", "", False, True, NormalizationType.to_lumi, 1,   0, 1, 1e-1, 1e12, "#gamma^{#mu}", "Entries", "_"+variant),
    
    Histogram("GoodInitialMuonsPair_deltaR"     , "", False, True, NormalizationType.to_lumi, 1, 0, 10, 10, 1e10, "#Delta R^{#mu#mu}", "Entries", "_"+variant),
    Histogram("GoodInitialMuonsPair_deltaEta"   , "", False, True, NormalizationType.to_lumi, 1, 0, 10, 1e0, 1e12, "#Delta #eta^{#mu#mu}", "Entries", "_"+variant),
    Histogram("GoodInitialMuonsPair_deltaPhi"   , "", False, True, NormalizationType.to_lumi, 1, 0, 3.14, 1e0, 1e12, "#Delta #phi^{#mu#mu}", "Entries", "_"+variant),
    Histogram("GoodInitialMuonsPair_mass"       , "", False, True, NormalizationType.to_lumi, 5, 10, 100, 1e-1, 1e10, "m^{#mu#mu} [GeV]", "Entries", "_"+variant),
    Histogram("GoodInitialMuonsPair_massCtauGt1cm"  , "", False, True, NormalizationType.to_lumi, 15, 10  , 100 , 1e-1, 1e8 , "m^{#mu#mu} [GeV]", "Entries", "_"+variant),
    Histogram("GoodInitialMuonsPair_massCtauGt1m"   , "", False, True, NormalizationType.to_lumi, 15, 10  , 100 , 1e-5, 1e8 , "m^{#mu#mu} [GeV]", "Entries", "_"+variant),
    Histogram("GoodInitialMuonsPair_massCtauGt10m"  , "", False, True, NormalizationType.to_lumi, 15, 10  , 100 , 1e-5, 1e8 , "m^{#mu#mu} [GeV]", "Entries", "_"+variant),
    Histogram("GoodInitialMuonsPair_muonsDistance"        , "", True , True, NormalizationType.to_lumi, 2, 1e-7, 1e7 , 1e-5, 1e12, "d(#mu_{1}, #mu_{2}) [m]", "Entries", "_"+variant),
    Histogram("GoodInitialMuonsPair_dimuonVertexD3D"        , "", True , True, NormalizationType.to_lumi, 1, 1e-8, 1e7 , 1e-5, 1e12, "d(#mu_{1}, #mu_{2}) [m]", "Entries", "_"+variant),
    
    Histogram("MuonsHittingDetector_energy", "", False, True, NormalizationType.to_lumi, 1,   30, 4000, 10, 2e14, "E^{#mu} [GeV]", "Entries", "_"+variant),
    Histogram("MuonsHittingDetector_pt", "", False, True, NormalizationType.to_lumi, 1,   0, 100, 10, 1e12, "p_{T}^{#mu} [GeV]", "Entries", "_"+variant),
    Histogram("MuonsHittingDetector_eta", "", False, True, NormalizationType.to_lumi, 1,   -10, 10, 1e0, 1e12, "#eta^{#mu}", "Entries", "_"+variant),
    Histogram("MuonsHittingDetector_d3d"                , "", True , True, NormalizationType.to_lumi, 2 , 1e-7, 1e3 , 1e-1, 1e8, "d_{3D}^{#mu} [m]", "Entries", "_"+variant),
    Histogram("MuonsHittingDetector_properCtau"                , "", True , True, NormalizationType.to_lumi, 2 , 1e-7, 1e3 , 1e-1, 1e8, "d_{3D}^{#mu} [m]", "Entries", "_"+variant),
    
    Histogram("MuonsHittingDetectorPair_mass"           , "", False, True, NormalizationType.to_lumi, 15, 10  , 100 , 1e-3, 1e6, "m^{#mu#mu} [GeV]", "Entries", "_"+variant),
    Histogram("MuonsHittingDetectorPair_massCtauGt1cm"  , "", False, True, NormalizationType.to_lumi, 15, 10  , 100 , 1e-5, 1e8 , "m^{#mu#mu} [GeV]", "Entries", "_"+variant),
    Histogram("MuonsHittingDetectorPair_massCtauGt1m"   , "", False, True, NormalizationType.to_lumi, 15, 10  , 100 , 1e-5, 1e8 , "m^{#mu#mu} [GeV]", "Entries", "_"+variant),
    Histogram("MuonsHittingDetectorPair_massCtauGt10m"  , "", False, True, NormalizationType.to_lumi, 15, 10  , 100 , 1e-5, 1e8 , "m^{#mu#mu} [GeV]", "Entries", "_"+variant),
    Histogram("MuonsHittingDetectorPair_muonsDistance"  , "", True , True, NormalizationType.to_lumi, 2, 1e-7, 1e7 , 1e-5, 1e12, "d(#mu_{1}, #mu_{2}) [m]", "Entries", "_"+variant),
    Histogram("MuonsHittingDetectorPair_dimuonVertexD3D", "", True , True, NormalizationType.to_lumi, 2, 9e-8, 1e3 , 1e-2, 1e8, "d^{#mu#mu}_{3D} [m]", "Entries", "_"+variant),
    
    Histogram("MuonsHittingDetectorSameVertexPair_mass"             , "", False, True, NormalizationType.to_lumi, 15, 10  , 100 , 1e-1, 1e8, "m^{#mu#mu} [GeV]", "Entries", "_"+variant),
    Histogram("MuonsHittingDetectorSameVertexPair_massCtauGt1cm"    , "", False, True, NormalizationType.to_lumi, 15, 10  , 100 , 1e-1, 1e8 , "m^{#mu#mu} [GeV]", "Entries", "_"+variant),
    Histogram("MuonsHittingDetectorSameVertexPair_massCtauGt1m"     , "", False, True, NormalizationType.to_lumi, 15, 10  , 100 , 1e-5, 1e8 , "m^{#mu#mu} [GeV]", "Entries", "_"+variant),
    Histogram("MuonsHittingDetectorSameVertexPair_massCtauGt10m"    , "", False, True, NormalizationType.to_lumi, 15, 10  , 100 , 1e-5, 1e8 , "m^{#mu#mu} [GeV]", "Entries", "_"+variant),
    Histogram("MuonsHittingDetectorSameVertexPair_muonsDistance"     , "", True , True, NormalizationType.to_lumi, 2, 1e-7, 1e7 , 1e-5, 1e12, "d(#mu_{1}, #mu_{2}) [m]", "Entries", "_"+variant),
    Histogram("MuonsHittingDetectorSameVertexPair_dimuonVertexD3D"  , "", True , True, NormalizationType.to_lumi, 2, 1e-7, 1e7 , 1e-5, 1e12, "d(#mu_{1}, #mu_{2}) [m]", "Entries", "_"+variant),
    
    
    

    # Histogram("GoodPtInitialMuons_energy", "", False, True, NormalizationType.to_lumi, 1,   30, 4000, 10, 2e14, "E^{#mu} [GeV]", "Entries", "_"+variant),
    # Histogram("GoodPtInitialMuons_pt", "", False, True, NormalizationType.to_lumi, 1,   0, 100, 10, 1e12, "p_{T}^{#mu} [GeV]", "Entries", "_"+variant),
    # Histogram("GoodPtInitialMuons_eta", "", False, True, NormalizationType.to_lumi, 1,   -10, 10, 1e0, 1e12, "#eta^{#mu}", "Entries", "_"+variant),
    # Histogram("GoodPtInitialMuons_d3d", "", True, True, NormalizationType.to_lumi, 1,   1e-7, 1e7, 5e-1, 1e10, "d_{3D}^{#mu} [m]", "Entries", "_"+variant),
    # Histogram("GoodPtInitialMuons_properCtau", "", True, True, NormalizationType.to_lumi, 1,   1e-7, 1e7, 5e-1, 1e10, "c#tau^{#mu} [m]", "Entries", "_"+variant),
    # Histogram("GoodPtInitialMuons_boost", "", False, True, NormalizationType.to_lumi, 1,   0, 1, 1e-1, 1e12, "#gamma^{#mu}", "Entries", "_"+variant),
    # Histogram("GoodPtInitialMuonsPair_deltaR", "", False, True, NormalizationType.to_lumi, 1,   0, 6, 10, 1e10, "#Delta R^{#mu#mu}", "Entries", "_"+variant),
    # Histogram("GoodPtInitialMuonsPair_deltaEta", "", False, True, NormalizationType.to_lumi, 1,   0, 10, 1e2, 1e11, "#Delta #eta^{#mu#mu}", "Entries", "_"+variant),
    # Histogram("GoodPtInitialMuonsPair_deltaPhi", "", False, True, NormalizationType.to_lumi, 1,   0, 3.14, 1e3, 1e10, "#Delta #phi^{#mu#mu}", "Entries", "_"+variant),
    # Histogram("GoodPtInitialMuonsPair_mass", "", False, True, NormalizationType.to_lumi, 5,   10, 100, 1e1, 1e11, "m^{#mu#mu} [GeV]", "Entries", "_"+variant),
    
    # Histogram("PtMuonsHittingDetector_d3d"                , "", True , True, NormalizationType.to_lumi, 2 , 1e-4, 1e3 , 1e-1, 1e8, "d_{3D}^{#mu} [m]", "Entries", "_"+variant),
    # Histogram("PtMuonsHittingDetectorPair_mass"           , "", False, True, NormalizationType.to_lumi, 15, 10  , 100 , 1e-1, 1e8, "m^{#mu#mu} [GeV]", "Entries", "_"+variant),
    
    

    # Histogram("DarkHadron_eta", "", False, True, NormalizationType.to_lumi, 1,   -10, 10, 1e1, 1e8, "#eta^{D}", "Entries", "_"+variant),
    # Histogram("DarkHadron_pt", "", False, True, NormalizationType.to_lumi, 1,   0, 150, 1e0, 1e6, "p_{T}^{D} [GeV]", "Entries", "_"+variant),

    # Histogram("DarkPhoton_eta", "", False, True, NormalizationType.to_lumi, 1,   -10, 10, 1e1, 1e6, "#eta^{A'}", "Entries", "_"+variant),
    # Histogram("DarkPhoton_phi", "", False, True, NormalizationType.to_lumi, 1,   -4, 4, 1e0, 1e6, "#phi^{A'}", "Entries", "_"+variant),
    # Histogram("DarkPhoton_pt", "", False, True, NormalizationType.to_lumi, 1,   0, 500, 1e0, 1e6, "p_{T}^{A'}", "Entries", "_"+variant),
    # Histogram("DarkPhoton_mass", "", False, True, NormalizationType.to_lumi, 1,   10, 100, 1e0, 1e6, "m^{A'} [GeV]", "Entries", "_"+variant),

    # Histogram("InitialMuons_energy", "", False, True, NormalizationType.to_lumi, 1,   0, 4000, 10, 1e12, "E^{#mu} [GeV]", "Entries", "_"+variant),
    # Histogram("InitialMuons_pt", "", False, True, NormalizationType.to_lumi, 1,   0, 100, 10, 1e12, "p_{T}^{#mu} [GeV]", "Entries", "_"+variant),
    # Histogram("InitialMuons_eta", "", False, True, NormalizationType.to_lumi, 1,   -10, 10, 1e0, 1e12, "#eta^{#mu}", "Entries", "_"+variant),
    # Histogram("InitialMuons_phi", "", False, True, NormalizationType.to_lumi, 1,   -12, 12, 1e-1, 1e12, "#phi^{#mu}", "Entries", "_"+variant),
    # Histogram("InitialMuons_x", "", True, True, NormalizationType.to_lumi, 1,   1e-7, 1e7, 5e-1, 1e10, "x^{#mu} [m]", "Entries", "_"+variant),
    # Histogram("InitialMuons_y", "", True, True, NormalizationType.to_lumi, 1,   1e-7, 1e7, 5e-1, 1e10, "y^{#mu} [m]", "Entries", "_"+variant),
    # Histogram("InitialMuons_z", "", True, True, NormalizationType.to_lumi, 1,   1e-5, 1e5, 5e1, 1e14, "z^{#mu} [m]", "Entries", "_"+variant),
    # Histogram("InitialMuonsPair_deltaR", "", False, True, NormalizationType.to_lumi, 1,   0, 6, 10, 1e10, "#Delta R^{#mu#mu}", "Entries", "_"+variant),
    # Histogram("InitialMuonsPair_deltaEta", "", False, True, NormalizationType.to_lumi, 1,   0, 20, 1e2, 1e9, "#Delta #eta^{#mu#mu}", "Entries", "_"+variant),
    # Histogram("InitialMuonsPair_deltaPhi", "", False, True, NormalizationType.to_lumi, 1,   0, 6, 1e2, 1e9, "#Delta #phi^{#mu#mu}", "Entries", "_"+variant),
    # Histogram("InitialMuonsPair_mass", "", False, True, NormalizationType.to_lumi, 5,   10, 100, 1e0, 1e10, "m^{#mu#mu} [GeV]", "Entries", "_"+variant),
    
    
    
    # Histogram("GoodInitialMuons_phi", "", False, True, NormalizationType.to_lumi, 1,   -12, 12, 1e-1, 1e12, "#phi^{#mu}", "Entries", "_"+variant),
    # Histogram("GoodInitialMuons_x", "", True, True, NormalizationType.to_lumi, 1,   1e-7, 1e7, 5e-1, 1e10, "x^{#mu} [m]", "Entries", "_"+variant),
    # Histogram("GoodInitialMuons_y", "", True, True, NormalizationType.to_lumi, 1,   1e-7, 1e7, 5e-1, 1e10, "y^{#mu} [m]", "Entries", "_"+variant),
    # Histogram("GoodInitialMuons_z", "", True, True, NormalizationType.to_lumi, 1,   1e-7, 1e7, 5e-1, 1e10, "z^{#mu} [m]", "Entries", "_"+variant),
    
    
    # Histogram("MuonsHittingDetector_energy", "", False, True, NormalizationType.to_lumi, 1,   0, 4000, 1e-1, 1e6, "E^{#mu}", "Entries", "_"+variant),
    # Histogram("MuonsHittingDetector_eta", "", False, True, NormalizationType.to_lumi, 1,   -12, 12, 1e-1, 1e6, "#eta^{#mu}", "Entries", "_"+variant),
    # Histogram("MuonsHittingDetectorPair_deltaR", "", False, True, NormalizationType.to_lumi, 1,   0, 6, 1e-1, 1e6, "#Delta R^{#mu#mu} [GeV]", "Entries", "_"+variant),
    
    
    # Histogram("Zprime_eta", "", False, True, NormalizationType.to_lumi, 1,   -12, 12, 1e-5, 1e6, "#eta^{Z'}", "Entries", "_"+variant),
    # Histogram("Zprime_pt", "", False, True, NormalizationType.to_lumi, 1,   0, 10, 1e-15, 1e6, "p_{T}^{Z'}", "Entries", "_"+variant),
    
    
    
)


output_formats = ["pdf"]

histogramsRatio = []

plotting_options = {
    SampleType.background: "hist",
    # SampleType.background: "hist nostack e",
    SampleType.signal: "nostack",
    SampleType.data: "",
}

canvas_size = (800, 600)
show_ratio_plots = False
ratio_limits = (0.0, 2.0)

show_cms_labels = False


legends = {
    SampleType.signal: Legend(0, 0, 10, 10, "l"),
    SampleType.data: Legend(0, 0, 10, 10, "l"),
    SampleType.background: Legend(0, 0, 10, 10, "f"),
}
