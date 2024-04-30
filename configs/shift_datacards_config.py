from Sample import Sample, SampleType
from Histogram import Histogram
from HistogramNormalizer import NormalizationType

from shift_paths import luminosity, crossSections, nGenEvents, base_path, processes, skim, histograms_path



add_uncertainties_on_zero = False
include_shapes = True

# signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7"
# signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3"
# signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1"
# signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0"
# signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1"
# signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2"
# signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3"
signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e5"

output_path = f"../datacards/limits_mass_{histograms_path.replace('histograms_', '')}_{signal_name.replace('pythia_', '')}"

samples = [
    Sample(
        name="pythia_qcd",
        file_path=f"{base_path}/pythia_qcd/merged_{skim}_{histograms_path}.root",
        type=SampleType.background,
        cross_sections=crossSections,
        initial_weight_sum=nGenEvents["pythia_qcd"],        
    ),
    Sample(
        name="pythia_dy",
        file_path=f"{base_path}/pythia_dy/merged_{skim}_{histograms_path}.root",
        type=SampleType.background,
        cross_sections=crossSections,
        initial_weight_sum=nGenEvents["pythia_dy"],
    ),
    Sample(
        name=f"signal_{signal_name}",
        file_path=f"{base_path}/{signal_name}/merged_{skim}_{histograms_path}.root",
        type=SampleType.signal,
        cross_sections=crossSections,
        initial_weight_sum=nGenEvents[signal_name],
    ),
]

# List histograms for which to create datacards 
histograms = [Histogram(name="MuonsHittingDetectorPair_mass", norm_type=NormalizationType.to_lumi, rebin=5)]

# List nuisance parameters (they will only be added for processes for which they were listed) 
nuisances = {
    "lumi": {
        "pythia_qcd": 1.015,
        "pythia_dy": 1.015,
        f"signal_{signal_name}": 1.015,
    },
    "other_systematics": {
        "pythia_qcd": 1.10,
        "pythia_dy": 1.10,
    }
}
