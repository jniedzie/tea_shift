import ROOT
from Sample import Sample, SampleType
from Legend import Legend
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType

from shift_paths import luminosity, crossSections, nGenEvents, base_path, processes, skim


output_path = f"../plots/{skim.replace('skimmed_', '')}/"

samples = (
    Sample(
        name="pythia_qcd",
        file_path="../histograms_qcd.root",
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
        file_path="../histograms_dy.root",
        type=SampleType.background,
        cross_sections=crossSections,
        initial_weight_sum=nGenEvents["pythia_dy"],

        fill_color=ROOT.kGreen,
        fill_alpha=1.0,
        marker_size=0.0,
        
        legend_description="DY",
        custom_legend=Legend(0.62, 0.65, 0.82, 0.70, "FL"),
    ),
     Sample(
        name="pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7",
        file_path="../histograms_signal.root",
        type=SampleType.signal,
        cross_sections=crossSections,
        initial_weight_sum=nGenEvents["pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7"],

        line_style=ROOT.kSolid,
        line_color=ROOT.kBlue,
        fill_alpha=0.0,
        marker_color=ROOT.kBlue,
        marker_style=20,
        marker_size=5.0,
        
        legend_description="100, 20, 1, 1e-7",
        custom_legend=Legend(0.62, 0.60, 0.82, 0.65, "L"),
    ),
)

custom_stacks_order = ["pythia_dy", "pythia_qcd", "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7"]


y_label = "Events"

histograms = (
    #           name                  title logx logy    norm_type                    rebin xmin   xmax  ymin    ymax,    xlabel                ylabel            suffix

    # photons
    Histogram("InitialMuonsPair_mass", "", False, True, NormalizationType.to_lumi, 1,   0, 100, 1e-1, 1e9, "m_{#mu#mu} (GeV)", "Entries", ""),
    Histogram("InitialMuonsPair_deltaR", "", False, True, NormalizationType.to_one, 1,   0, 10, 1e-6, 1e0, "#Delta R_{#mu#mu} (GeV)", "Entries", ""),
   
    Histogram("MuonsHittingDetectorPair_mass", "", False, True, NormalizationType.to_lumi, 1,   0, 100, 1e-1, 1e9, "m_{#mu#mu} (GeV)", "Entries", ""),
    Histogram("MuonsHittingDetectorPair_deltaR", "", False, True, NormalizationType.to_one, 1,   0, 10, 1e-6, 1e0, "#Delta R_{#mu#mu} (GeV)", "Entries", ""),
   
    Histogram("cutFlow", "", False, True, NormalizationType.to_lumi, 1, 0, 10, 1e1, 1e7, "Selection", "#sum genWeight"),
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
