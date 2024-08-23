from Sample import Sample, SampleType
from Histogram import Histogram
from HistogramNormalizer import NormalizationType

from shift_paths import luminosity, crossSections, base_datacard_name
from shift_paths import base_path, processes, histograms_path, colliderMode
from shift_utils import get_file_name

add_uncertainties_on_zero = False
include_shapes = True

signal_name = "dummy_value"
variant_name = "dummy_value"
signal_file_name = signal_name.replace("pythia_", "pythiaCollider_") if colliderMode else signal_name
output_path = f"../datacards/{base_datacard_name.format(get_file_name(signal_name, variant_name))}"
signal_key = signal_name if signal_name in crossSections else signal_name.replace("Collider", "")

qcd_suffix = ""
# qcd_suffix = "_ptHat10GeV"
# qcd_suffix = "_ptHat5GeV"

qcd_sample_name = f"pythia{'Collider' if colliderMode else ''}_qcd{qcd_suffix}"

samples = [
    Sample(
        name=qcd_sample_name,
        file_path=f"{base_path}/{qcd_sample_name}/merged_{variant_name}_histograms.root",
        type=SampleType.background,
        cross_sections=crossSections,
    ),
    Sample(
        name=f"pythia{'Collider' if colliderMode else ''}_dy",
        file_path=f"{base_path}/pythia{'Collider' if colliderMode else ''}_dy/merged_{variant_name}_histograms.root",
        type=SampleType.background,
        cross_sections=crossSections,
    ),
    Sample(
        name=f"signal_{signal_name}",
        file_path=f"{base_path}/{signal_file_name}/merged_{variant_name}_histograms.root",
        type=SampleType.signal,
        cross_section=crossSections[signal_key.replace('_smallCoupling', '')],
    ),
]

# List histograms for which to create datacards 

histograms = [Histogram(name="dummy_value", norm_type=NormalizationType.to_lumi, rebin=5)]

# List nuisance parameters (they will only be added for processes for which they were listed) 
nuisances = {
    "lumi": {
        qcd_sample_name: 1.015,
        f"pythia{'Collider' if colliderMode else ''}_dy": 1.015,
        f"signal_{signal_name}": 1.015,
    },
    "other_systematics": {
        qcd_sample_name: 1.10,
        f"pythia{'Collider' if colliderMode else ''}_dy": 1.10,
    }
}
