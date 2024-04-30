import ROOT
from Sample import Sample, SampleType
from Legend import Legend
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType

from shift_paths import luminosity, crossSections, nGenEvents, base_path, processes, skim, histograms_path


output_path = f"../plots/{skim.replace('skimmed_', '')}/"

samples = [
    Sample(
        name="pythia_qcd",
        file_path=f"{base_path}/pythia_qcd/merged_{skim}_{histograms_path}.root",
        type=SampleType.background,
        cross_sections=crossSections,
        initial_weight_sum=nGenEvents["pythia_qcd"],        
        
        fill_color=ROOT.kYellow,
        fill_alpha=1.0,
        marker_size=0.0,
        
        legend_description="QCD",
        custom_legend=Legend(0.62, 0.70, 0.82, 0.75, "FL"),
    ),
    Sample(
        name="pythia_dy",
        file_path=f"{base_path}/pythia_dy/merged_{skim}_{histograms_path}.root",
        type=SampleType.background,
        cross_sections=crossSections,
        initial_weight_sum=nGenEvents["pythia_dy"],

        fill_color=ROOT.kGreen,
        fill_alpha=1.0,
        marker_size=0.0,
        
        legend_description="DY",
        custom_legend=Legend(0.62, 0.65, 0.82, 0.70, "FL"),
    ),
]

custom_stacks_order = ["pythia_dy", "pythia_qcd"]

def addSignalSample(name, color, legend_y):
    samples.append(Sample(
        name=name,
        file_path=f"{base_path}/{name}/merged_{skim}_{histograms_path}.root",
        type=SampleType.signal,
        cross_sections=crossSections,
        initial_weight_sum=nGenEvents[name],
        line_alpha=1,
        line_style=1,
        fill_alpha=0,
        marker_size=0,
        line_color=color,
        legend_description=name.replace("pythia_mZprime", ""),
        custom_legend=Legend(0.50, legend_y, 0.82, legend_y+0.03, "L"),
    )
    )
    
    custom_stacks_order.append(name)

addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7", ROOT.kViolet, 0.60)
addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3", ROOT.kBlue, 0.57)
addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1", ROOT.kCyan, 0.54)
addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0", ROOT.kGreen, 0.51)
addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1", ROOT.kGreen+1, 0.48)
addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2", ROOT.kOrange, 0.45)
addSignalSample("pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3", ROOT.kRed, 0.42)




y_label = "Events"

histograms = (
    #           name                  title logx logy    norm_type                    rebin xmin   xmax  ymin    ymax,    xlabel                ylabel            suffix

    # photons
    Histogram("InitialMuonsPair_mass", "", False, True, NormalizationType.to_lumi, 1,   0, 100, 1e-1, 1e10, "m_{#mu#mu} (GeV)", "Entries", ""),
    Histogram("InitialMuonsPair_deltaR", "", False, True, NormalizationType.to_lumi, 1,   0, 10, 1e-1, 1e10, "#Delta R_{#mu#mu} (GeV)", "Entries", ""),
    Histogram("InitialMuonsPair_lowMass", "", False, True, NormalizationType.to_lumi, 4,   0, 5, 1e-1, 1e10, "m_{#mu#mu} (GeV)", "Entries", ""),
   
    Histogram("MuonsHittingDetectorPair_mass", "", False, True, NormalizationType.to_lumi, 5,   0, 30, 1e-1, 1e9, "m_{#mu#mu} (GeV)", "Entries", ""),
    Histogram("MuonsHittingDetectorPair_deltaR", "", False, True, NormalizationType.to_lumi, 1,   0, 10, 1e-1, 1e9, "#Delta R_{#mu#mu} (GeV)", "Entries", ""),
   
    Histogram("cutFlow", "", False, True, NormalizationType.to_lumi, 1, 0, 10, 1e1, 1e7, "Selection", "#sum genWeight"),
    
    Histogram("Event_count", "", False, True, NormalizationType.to_lumi, 1, 0, 1, 1e-1, 1e10, "", "#events"),
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
