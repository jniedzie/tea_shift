import ROOT
from Sample import Sample, SampleType
from Legend import Legend
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType

from shift_paths import crossSections, base_path, variant, colliderMode, luminosity

variant = "shift120m"
# variant = "shift250m"
# variant = "shift300m"

output_path = f"../plots/signals_comparison_{variant}/"

legend_x_1 = 0.20
legend_x_2 = 0.45
legend_x_3 = 0.65

legend_max_y = 0.89

legend_width = 0.15
legend_height = 0.04

signal_ref_cross_section = 20e-5

samples = []
custom_stacks_order = []

custom_titles = {
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1": "default (100, 20, 1)",
    
    "pythia_mZprime-40_mDH-20_mDQ-1_tau-1e1": "m_{Z'}= 40 GeV",
    "pythia_mZprime-50_mDH-20_mDQ-1_tau-1e1": "m_{Z'}= 50 GeV",
    "pythia_mZprime-110_mDH-20_mDQ-1_tau-1e1": "m_{Z'}= 110 GeV",
    
    "pythia_mZprime-200_mDH-20_mDQ-1_tau-1e1": "m_{Z'}= 200 GeV",
    "pythia_mZprime-500_mDH-20_mDQ-1_tau-1e1": "m_{Z'}= 500 GeV",
    
    "pythia_mZprime-100_mDH-15_mDQ-1_tau-1e1": "m_{D}= 15 GeV",
    "pythia_mZprime-100_mDH-40_mDQ-1_tau-1e1": "m_{D}= 40 GeV",
    "pythia_mZprime-100_mDH-60_mDQ-1_tau-1e1": "m_{D}= 60 GeV",
    
    "pythia_mZprime-100_mDH-20_mDQ-2_tau-1e1": "m_{q}= 2 GeV",
    "pythia_mZprime-100_mDH-20_mDQ-5_tau-1e1": "m_{q}= 5 GeV",
    "pythia_mZprime-100_mDH-20_mDQ-10_tau-1e1": "m_{q}= 10 GeV",
    
    "pythia_mZprime-20_mDH-5_mDQ-1_tau-1e1": "m_{Z'}= 20, m_{D}= 5",
    "pythia_mZprime-100_mDH-15_mDQ-7_tau-1e1": "m_{D}= 15, m_{q}= 7",
    "pythia_mZprime-30_mDH-15_mDQ-7_tau-1e1": "m_{Z'}= 30, m_{D}= 15, m_{q}= 7",
    
    "pythia_mZprime-40_mDH-20_mDQ-10_tau-1e1": "40/20/10",
}

def addSignalSample(name, color, marker_style, marker_size, legend_x, legend_y):
    
    file_name = name.replace("pythia_", "pythiaCollider_") if colliderMode else name

    samples.append(Sample(
        name=name,
        file_path=f"{base_path}/{file_name}/merged_{variant}_histograms.root",
        type=SampleType.signal,
        cross_section=signal_ref_cross_section,
        line_alpha=1,
        line_color=color,
        fill_alpha=0,
        marker_style=marker_style,
        marker_size=marker_size,
        marker_color=color,
        legend_description=custom_titles[name],
        custom_legend=Legend(legend_x, legend_y, legend_x+legend_width, legend_y+legend_height, "PL"),
    )
    )
    
    custom_stacks_order.append(name)


addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1", ROOT.kBlack, 20, 1.5, legend_x_1, legend_max_y-1*legend_height)
addSignalSample("pythia_mZprime-20_mDH-5_mDQ-1_tau-1e1", ROOT.kViolet, 24, 1.0, legend_x_1, legend_max_y-2*legend_height)
addSignalSample("pythia_mZprime-100_mDH-15_mDQ-7_tau-1e1", ROOT.kBlue, 24, 1.0, legend_x_1, legend_max_y-3*legend_height)
addSignalSample("pythia_mZprime-30_mDH-15_mDQ-7_tau-1e1", ROOT.kGreen+1, 24, 1.0, legend_x_1, legend_max_y-4*legend_height)

addSignalSample("pythia_mZprime-40_mDH-20_mDQ-1_tau-1e1", ROOT.kBlue, 21, 1.0, legend_x_2, legend_max_y-1*legend_height)
addSignalSample("pythia_mZprime-50_mDH-20_mDQ-1_tau-1e1", ROOT.kCyan, 21, 1.0, legend_x_2, legend_max_y-2*legend_height)
addSignalSample("pythia_mZprime-110_mDH-20_mDQ-1_tau-1e1", ROOT.kCyan+1, 21, 1.0, legend_x_2, legend_max_y-3*legend_height)

addSignalSample("pythia_mZprime-40_mDH-20_mDQ-10_tau-1e1", ROOT.kBlack, 24, 1.0, legend_x_2, legend_max_y-4*legend_height)

addSignalSample("pythia_mZprime-100_mDH-15_mDQ-1_tau-1e1", ROOT.kRed , 22, 1.0, legend_x_3, legend_max_y-1*legend_height)
addSignalSample("pythia_mZprime-100_mDH-40_mDQ-1_tau-1e1", ROOT.kOrange, 22, 1.0, legend_x_3, legend_max_y-2*legend_height)
addSignalSample("pythia_mZprime-100_mDH-60_mDQ-1_tau-1e1", ROOT.kMagenta, 22, 1.0, legend_x_3, legend_max_y-3*legend_height)

addSignalSample("pythia_mZprime-100_mDH-20_mDQ-2_tau-1e1", ROOT.kGreen ,23, 1.0, legend_x_3, legend_max_y-4*legend_height)
addSignalSample("pythia_mZprime-100_mDH-20_mDQ-5_tau-1e1", ROOT.kGreen+1, 23, 1.0, legend_x_3, legend_max_y-5*legend_height)
addSignalSample("pythia_mZprime-100_mDH-20_mDQ-10_tau-1e1", ROOT.kCyan, 23, 1.0, legend_x_3, legend_max_y-6*legend_height)






y_label = "Events"

histograms = (

    Histogram("cutFlow", "", False, True, NormalizationType.to_lumi, 1, 0, 6, 1e0, 1e4, "Selection", "#sum genWeight"),

    Histogram("DarkHadron_eta", "", False, True, NormalizationType.to_lumi, 1,   0, 12, 1e-3, 1e6, "#eta^{D}", "Entries", ""),
    Histogram("DarkHadron_pt", "", False, True, NormalizationType.to_lumi, 1,   0, 200, 1e-5, 1e6, "p_{T}^{D}", "Entries", ""),

    Histogram("Event_nDarkHadrons", "", False, True, NormalizationType.to_lumi, 1,   0, 7, 1e-1, 1e4, "#Dark Hadrons", "Entries", ""),
    Histogram("Event_nInitialMuons", "", False, True, NormalizationType.to_lumi, 1,   0, 10, 1e-3, 1e6, "#Initial Muons", "Entries", ""),
    Histogram("Event_nMuonsHittingDetector", "", False, True, NormalizationType.to_lumi, 1,   0, 10, 1e-5, 1e6, "#Passing Muons", "Entries", ""),
    Histogram("Event_nZprimes", "", False, True, NormalizationType.to_lumi, 1,   0, 10, 1e-15, 1e6, "#Z'", "Entries", ""),

    Histogram("InitialMuons_energy", "", False, True, NormalizationType.to_lumi, 1,   0, 4000, 1e-1, 1e4, "E^{#mu}", "Entries", ""),
    Histogram("InitialMuons_eta", "", False, False, NormalizationType.to_one, 1,   -2, 13, 0, 0.2, "#eta^{#mu}", "Entries", ""),
    Histogram("InitialMuonsPair_deltaR", "", False, False, NormalizationType.to_one, 1,   0, 6, 0, 0.15, "#Delta R^{#mu#mu}", "Entries", ""),
    Histogram("InitialMuonsPair_mass", "", True, True, NormalizationType.to_lumi, 1,   10, 100, 5e-3, 1e4, "m^{#mu#mu} (GeV)", "Entries", ""),
    
    Histogram("MuonsHittingDetector_energy", "", False, True, NormalizationType.to_lumi, 1,   0, 4000, 1e-3, 1e5, "E^{#mu}", "Entries", ""),
    Histogram("MuonsHittingDetector_eta", "", False, True, NormalizationType.to_lumi, 1,   -2, 12, 1e-4, 1e10, "#eta^{#mu}", "Entries", ""),
    Histogram("MuonsHittingDetectorPair_deltaR", "", False, True, NormalizationType.to_lumi, 1,   0, 6, 1e-3, 1e3, "#Delta R^{#mu#mu} (GeV)", "Entries", ""),
    Histogram("MuonsHittingDetectorPair_mass", "", False, True, NormalizationType.to_lumi, 5,   10, 100, 1e-4, 10, "m^{#mu#mu} (GeV)", "Entries", ""),
    
    Histogram("Zprime_eta", "", False, True, NormalizationType.to_lumi, 1,   2, 15, 1e-3, 1e6, "#eta^{Z'}", "Entries", ""),
    Histogram("Zprime_pt", "", False, True, NormalizationType.to_lumi, 1,   0, 100, 1e-5, 1e6, "p_{T}^{Z'}", "Entries", ""),
    
    
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

