import ROOT
from Sample import Sample, SampleType
from Legend import Legend
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType

from shift_paths import crossSections, base_path, variant, colliderMode, luminosity
from shift_paths import crossSections, base_path, luminosity

# variant = "cms"
# colliderMode = True
output_path = f"../plots/{variant}/"

backgrounds_legend_x = 0.50
signals_legend_x = 0.65

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

custom_stacks_order = ["pythia_dy", "pythia_qcd"]

custom_titles = {
    "pythia_mZprime-50_mDH-20_mDQ-1_tau-1e1": "m_{Z'}= 50 GeV",
    "pythia_mZprime-200_mDH-20_mDQ-1_tau-1e1": "m_{Z'}= 200 GeV",
    "pythia_mZprime-500_mDH-20_mDQ-1_tau-1e1": "m_{Z'}= 500 GeV",
    "pythia_mZprime-100_mDH-15_mDQ-1_tau-1e1": "m_{D}= 15 GeV",
    "pythia_mZprime-100_mDH-40_mDQ-1_tau-1e1": "m_{D}= 40 GeV",
    "pythia_mZprime-100_mDH-60_mDQ-1_tau-1e1": "m_{D}= 60 GeV",
    "pythia_mZprime-100_mDH-20_mDQ-2_tau-1e1": "m_{q}= 2 GeV",
    "pythia_mZprime-100_mDH-20_mDQ-5_tau-1e1": "m_{q}= 5 GeV",
    "pythia_mZprime-20_mDH-5_mDQ-1_tau-1e1": "m_{Z'}= 20, m_{D}= 5",
    "pythia_mDarkPhoton-5": "m_{A'}= 5 GeV",
    "pythia_mDarkPhoton-30": "m_{A'}= 30 GeV",
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
        title += "} (m)"
    
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

# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7", ROOT.kViolet, legend_max_y-legend_height)
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3", ROOT.kBlue, legend_max_y-2*legend_height)
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1", ROOT.kCyan, legend_max_y-3*legend_height)
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0", ROOT.kGreen, legend_max_y-4*legend_height)
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1", ROOT.kGreen+1, legend_max_y-5*legend_height)
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2", ROOT.kOrange, legend_max_y-6*legend_height)
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3", ROOT.kRed, legend_max_y-7*legend_height)
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e5", ROOT.kMagenta, legend_max_y-8*legend_height)

# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-10_tau-1em7", ROOT.kViolet, legend_max_y-1*legend_height)
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-10_tau-1em1", ROOT.kCyan, legend_max_y-2*legend_height)
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-10_tau-1e0", ROOT.kBlue, legend_max_y-3*legend_height)
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-10_tau-1e1", ROOT.kOrange, legend_max_y-4*legend_height)
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-10_tau-1e3", ROOT.kRed, legend_max_y-5*legend_height)
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-10_tau-1e5", ROOT.kMagenta, legend_max_y-6*legend_height)

# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-10_tau-1em1", ROOT.kViolet, legend_max_y-1*legend_height, "shift120m")
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-10_tau-1em1", ROOT.kCyan, legend_max_y-2*legend_height, "shift200m")
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-10_tau-1em1", ROOT.kBlue, legend_max_y-3*legend_height, "shift290m")
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-10_tau-1em1", ROOT.kOrange, legend_max_y-4*legend_height, "shift300m")
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-10_tau-1em1", ROOT.kRed, legend_max_y-5*legend_height, "shift310m")

# addSignalSample("pythia_mZprime-110_mDH-20_mDQ-1_tau-1em1", ROOT.kViolet, legend_max_y-legend_height)
# addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1", ROOT.kBlue, legend_max_y-2*legend_height)
# addSignalSample("pythia_mZprime-90_mDH-20_mDQ-1_tau-1em1", ROOT.kCyan, legend_max_y-3*legend_height)
# addSignalSample("pythia_mZprime-80_mDH-20_mDQ-1_tau-1em1", ROOT.kGreen, legend_max_y-4*legend_height)
# addSignalSample("pythia_mZprime-70_mDH-20_mDQ-1_tau-1em1", ROOT.kGreen+1, legend_max_y-5*legend_height)
# addSignalSample("pythia_mZprime-60_mDH-20_mDQ-1_tau-1em1", ROOT.kOrange, legend_max_y-6*legend_height)
# addSignalSample("pythia_mZprime-50_mDH-20_mDQ-1_tau-1em1", ROOT.kRed, legend_max_y-7*legend_height)

# addSignalSample("pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em5", ROOT.kViolet, legend_max_y-legend_height)
# addSignalSample("pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em3", ROOT.kBlue, legend_max_y-2*legend_height)
# addSignalSample("pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em1", ROOT.kCyan, legend_max_y-3*legend_height)
# addSignalSample("pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e0", ROOT.kGreen, legend_max_y-4*legend_height)
# addSignalSample("pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e1", ROOT.kGreen+1, legend_max_y-5*legend_height)
# addSignalSample("pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e3", ROOT.kOrange, legend_max_y-6*legend_height)
# addSignalSample("pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e5", ROOT.kRed, legend_max_y-7*legend_height)

addSignalSample("pythia_mDarkPhoton-5_ctau-1e1", ROOT.kViolet, legend_max_y-legend_height)
addSignalSample("pythia_mDarkPhoton-10_ctau-1e1", ROOT.kBlue, legend_max_y-2*legend_height)
addSignalSample("pythia_mDarkPhoton-15_ctau-1e1", ROOT.kCyan, legend_max_y-3*legend_height)
addSignalSample("pythia_mDarkPhoton-20_ctau-1e1", ROOT.kGreen, legend_max_y-4*legend_height)
addSignalSample("pythia_mDarkPhoton-30_ctau-1e1", ROOT.kGreen+1, legend_max_y-5*legend_height)
addSignalSample("pythia_mDarkPhoton-40_ctau-1e1", ROOT.kOrange, legend_max_y-6*legend_height)
addSignalSample("pythia_mDarkPhoton-70_ctau-1e1", ROOT.kRed, legend_max_y-7*legend_height)

y_label = "Events"

histograms = (

    Histogram("cutFlow", "", False, True, NormalizationType.to_lumi, 1, 0, 7, 1e-5, 1e10, "Selection", "#sum genWeight"),

    Histogram("DarkHadron_eta", "", False, True, NormalizationType.to_lumi, 1,   -2, 12, 1e-5, 1e6, "#eta^{D}", "Entries", ""),
    Histogram("DarkHadron_pt", "", False, True, NormalizationType.to_lumi, 1,   0, 200, 1e-5, 1e6, "p_{T}^{D} (GeV)", "Entries", ""),

    Histogram("InitialMuons_energy", "", False, True, NormalizationType.to_lumi, 1,   0, 4000, 10, 1e12, "E^{#mu} (GeV)", "Entries", ""),
    Histogram("InitialMuons_pt", "", False, True, NormalizationType.to_lumi, 1,   0, 4000, 10, 1e12, "p_{T}^{#mu} (GeV)", "Entries", ""),
    Histogram("InitialMuons_eta", "", False, True, NormalizationType.to_lumi, 1,   -12, 12, 1e-1, 1e12, "#eta^{#mu}", "Entries", ""),
    Histogram("InitialMuons_phi", "", False, True, NormalizationType.to_lumi, 1,   -12, 12, 1e-1, 1e12, "#phi^{#mu}", "Entries", ""),
    
    Histogram("InitialMuons_x", "", True, True, NormalizationType.to_lumi, 1,   1e10, 1e11, 5e-1, 1e10, "x^{#mu} (m)", "Entries", ""),
    Histogram("InitialMuons_y", "", True, True, NormalizationType.to_lumi, 1,   1e10, 1e11, 5e-1, 1e10, "y^{#mu} (m)", "Entries", ""),
    Histogram("InitialMuons_z", "", True, True, NormalizationType.to_lumi, 1,   1e10, 1e11, 5e-1, 1e10, "z^{#mu} (m)", "Entries", ""),
    
    Histogram("InitialMuonsPair_deltaR", "", False, True, NormalizationType.to_lumi, 1,   0, 6, 10, 1e10, "#Delta R^{#mu#mu}", "Entries", ""),
    # Histogram("InitialMuonsPair_deltaEta", "", False, True, NormalizationType.to_lumi, 1,   0, 6, 10, 1e10, "#Delta #eta^{#mu#mu}", "Entries", ""),
    # Histogram("InitialMuonsPair_deltaPhi", "", False, True, NormalizationType.to_lumi, 1,   0, 6, 10, 1e10, "#Delta #phi^{#mu#mu}", "Entries", ""),
    Histogram("InitialMuonsPair_mass", "", False, True, NormalizationType.to_lumi, 5,   10, 100, 1e0, 1e10, "m^{#mu#mu} (GeV)", "Entries", ""),
    
    Histogram("MuonsHittingDetector_energy", "", False, True, NormalizationType.to_lumi, 1,   0, 4000, 1e-1, 1e6, "E^{#mu}", "Entries", ""),
    Histogram("MuonsHittingDetector_eta", "", False, True, NormalizationType.to_lumi, 1,   -12, 12, 1e-1, 1e6, "#eta^{#mu}", "Entries", ""),
    Histogram("MuonsHittingDetectorPair_deltaR", "", False, True, NormalizationType.to_lumi, 1,   0, 6, 1e-1, 1e6, "#Delta R^{#mu#mu} (GeV)", "Entries", ""),
    Histogram("MuonsHittingDetectorPair_mass", "", False, True, NormalizationType.to_lumi, 10,   0, 100, 1e-2, 1e6, "m^{#mu#mu} (GeV)", "Entries", ""),
    
    Histogram("Zprime_eta", "", False, True, NormalizationType.to_lumi, 1,   4, 12, 1e-5, 1e6, "#eta^{Z'}", "Entries", ""),
    Histogram("Zprime_pt", "", False, True, NormalizationType.to_lumi, 1,   0, 10, 1e-15, 1e6, "p_{T}^{Z'}", "Entries", ""),
    
    Histogram("DarkPhoton_eta", "", False, True, NormalizationType.to_lumi, 1,   -10, 10, 1e-2, 1e4, "#eta^{A'}", "Entries", ""),
    Histogram("DarkPhoton_phi", "", False, True, NormalizationType.to_lumi, 1,   -10, 10, 1e-2, 1e4, "#phi^{A'}", "Entries", ""),
    Histogram("DarkPhoton_pt", "", False, True, NormalizationType.to_lumi, 1,   0, 1000, 1e-4, 1e4, "p_{T}^{A'}", "Entries", ""),
    Histogram("DarkPhoton_mass", "", False, True, NormalizationType.to_lumi, 1,   10, 100, 1e0, 1e10, "m^{A'} (GeV)", "Entries", ""),
    
)


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
