import ROOT
from Sample import Sample, SampleType
from Legend import Legend
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType

from shift_paths import crossSections, base_path, variant, colliderMode, luminosity

output_path = f"../plots/{variant}/"

backgrounds_legend_x = 0.50
signals_legend_x = 0.65

legend_max_y = 0.89

legend_width = 0.15
legend_height = 0.04

signal_ref_cross_section = 2e-5

samples = [
    Sample(
        name="pythia_qcd",
        file_path=f"{base_path}/pythia{'Collider' if colliderMode else ''}_qcd/merged_{variant}_histograms.root",
        type=SampleType.background,
        cross_sections=crossSections,
        
        fill_color=ROOT.kRed+1,
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

        fill_color=ROOT.kGreen+1,
        fill_alpha=1.0,
        marker_size=0.0,
        
        legend_description="DY",
        custom_legend=Legend(backgrounds_legend_x, legend_max_y-2*legend_height, backgrounds_legend_x+legend_width, legend_max_y-legend_height, "FL"),
    ),
]

custom_stacks_order = ["pythia_dy", "pythia_qcd"]

def addSignalSample(name, color, legend_y):
    
    file_name = name.replace("pythia_", "pythiaCollider_") if colliderMode else name
    title = name.replace("pythia_mZprime-100_mDH-20_mDQ-1_", "")
    title = title.replace("tau-", "c#tau=")
    title = title.replace("1em", "10^{-")
    title = title.replace("1e", "10^{")
    title += "} (m)"
    
    samples.append(Sample(
        name=name,
        file_path=f"{base_path}/{file_name}/merged_{variant}_histograms.root",
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
    
    custom_stacks_order.append(name)

addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7", ROOT.kViolet, legend_max_y-legend_height)
addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3", ROOT.kBlue, legend_max_y-2*legend_height)
addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1", ROOT.kCyan, legend_max_y-3*legend_height)
addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0", ROOT.kGreen, legend_max_y-4*legend_height)
addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1", ROOT.kGreen+1, legend_max_y-5*legend_height)
addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2", ROOT.kOrange, legend_max_y-6*legend_height)
addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3", ROOT.kRed, legend_max_y-7*legend_height)
addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e5", ROOT.kMagenta, legend_max_y-8*legend_height)




y_label = "Events"

histograms = (

    Histogram("cutFlow", "", False, True, NormalizationType.to_lumi, 1, 0, 6, 1e1, 1e10, "Selection", "#sum genWeight"),

    Histogram("DarkHadron_eta", "", False, True, NormalizationType.to_lumi, 1,   -2, 12, 1e-5, 1e6, "#eta^{D}", "Entries", ""),
    Histogram("DarkHadron_pt", "", False, True, NormalizationType.to_lumi, 1,   0, 200, 1e-5, 1e6, "p_{T}^{D}", "Entries", ""),

    Histogram("InitialMuons_energy", "", False, True, NormalizationType.to_lumi, 1,   0, 4000, 10, 1e12, "E^{#mu}", "Entries", ""),
    Histogram("InitialMuons_eta", "", False, True, NormalizationType.to_lumi, 1,   -2, 12, 1e0, 1e10, "#eta^{#mu}", "Entries", ""),
    Histogram("InitialMuonsPair_deltaR", "", False, True, NormalizationType.to_lumi, 1,   0, 6, 10, 1e10, "#Delta R^{#mu#mu}", "Entries", ""),
    Histogram("InitialMuonsPair_mass", "", False, True, NormalizationType.to_lumi, 5,   10, 40, 5e-1, 1e6, "m^{#mu#mu} (GeV)", "Entries", ""),
    
    Histogram("MuonsHittingDetector_energy", "", False, True, NormalizationType.to_lumi, 1,   0, 4000, 1e-5, 1e5, "E^{#mu}", "Entries", ""),
    Histogram("MuonsHittingDetector_eta", "", False, True, NormalizationType.to_lumi, 1,   -2, 12, 1e-10, 1e10, "#eta^{#mu}", "Entries", ""),
    Histogram("MuonsHittingDetectorPair_deltaR", "", False, True, NormalizationType.to_lumi, 1,   0, 10, 1e-5, 1e5, "#Delta R^{#mu#mu} (GeV)", "Entries", ""),
    Histogram("MuonsHittingDetectorPair_mass", "", False, True, NormalizationType.to_lumi, 5,   10, 40, 1e-5, 10, "m^{#mu#mu} (GeV)", "Entries", ""),
    
    Histogram("Zprime_eta", "", False, True, NormalizationType.to_lumi, 1,   4, 12, 1e-5, 1e6, "#eta^{Z'}", "Entries", ""),
    Histogram("Zprime_pt", "", False, True, NormalizationType.to_lumi, 1,   0, 10, 1e-15, 1e6, "p_{T}^{Z'}", "Entries", ""),
    
    
    
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
