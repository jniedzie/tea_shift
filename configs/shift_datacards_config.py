from Sample import Sample, SampleType
from Histogram import Histogram
from HistogramNormalizer import NormalizationType

from shift_paths import luminosity, crossSections, base_datacard_name
from shift_paths import base_path, processes, histograms_path, colliderMode, variant
from shift_utils import get_file_name

add_uncertainties_on_zero = False
include_shapes = True

# variant = "shift500m"
signal_name = "dummy_value"

# signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7"
# signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3"
# signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1"
# signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0"
# signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1"
# signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2"
# signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3"
# signal_name = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e5"


signal_file_name = signal_name.replace("pythia_", "pythiaCollider_") if colliderMode else signal_name

output_path = f"../datacards/{base_datacard_name.format(get_file_name(signal_name))}"

signal_key = signal_name if signal_name in crossSections else signal_name.replace("Collider", "")

samples = [
    Sample(
        name="pythia_qcd",
        file_path=f"{base_path}/pythia{'Collider' if colliderMode else ''}_qcd/merged_{variant}_histograms.root",
        type=SampleType.background,
        cross_sections=crossSections,
    ),
    Sample(
        name="pythia_dy",
        file_path=f"{base_path}/pythia{'Collider' if colliderMode else ''}_dy/merged_{variant}_histograms.root",
        type=SampleType.background,
        cross_sections=crossSections,
    ),
    Sample(
        name=f"signal_{signal_name}",
        file_path=f"{base_path}/{signal_file_name}/merged_{variant}_histograms.root",
        type=SampleType.signal,
        cross_section=crossSections[signal_key],
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
