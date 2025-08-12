import ROOT
from Sample import Sample, SampleType
from Legend import Legend
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType

from shift_neutrinos_paths import crossSections, base_path, variant, luminosity

output_path = f"../plots/neutrinos_{variant}/"

backgrounds_legend_x = 0.58
signals_legend_x = 0.20

legend_max_y = 0.89

legend_width = 0.08
legend_height = 0.035

if variant == "shift160m":
  qcd_bins = [
    "_ptHat20toInfGeV",
    "_ptHat10to20GeV",
    "_ptHat5to10GeV",
    "_ptHat2to5GeV",
    "_ptHat1to2GeV",
    "_ptHat0to1GeV",  # zero events passing
  ]
else:
  qcd_bins = [
    "_ptHat0to10GeV",
    "_ptHat10to20GeV",
    
    "_ptHat50to100GeV",
    "_ptHat100toInfGeV",
  ]

# for unbinned QCD samples:
# qcd_bins = [""]

samples = [
  Sample(
    name="pythia_dy",
    file_path=f"{base_path}/pythia{'Collider' if variant == 'FASER' else ''}_dy/merged_{variant}_neutrinos_histograms.root",
    type=SampleType.background,
    cross_sections=crossSections,
    fill_color=ROOT.kGray + 1,
    fill_alpha=1.0,
    marker_size=0.0,
    legend_description="DY",
    custom_legend=Legend(
      backgrounds_legend_x, legend_max_y - 1 * legend_height,
      backgrounds_legend_x + legend_width, legend_max_y - 0 * legend_height,
      "FL"
    ),
  ),
]

custom_stacks_order = ["pythia_dy"]

qcd_colors = [
  ROOT.kRed, ROOT.kGreen, ROOT.kBlue, ROOT.kOrange, ROOT.kMagenta, ROOT.kCyan
]


def get_nice_qcd_name(suffix):
  import re

  match = re.search(r'_ptHat(\d*)to(\d+|Inf)GeV', suffix)
  if match:
    low, high = match.groups()
    if not low:
      return "QCD"
    low_val = int(low)
    if high == 'Inf':
      return f"QCD p_{{#hat{{T}}}} > {low_val} GeV"
    else:
      high_val = int(high)
      return f"QCD p_{{#hat{{T}}}} #in ({low_val}, {high_val}] GeV"
  else:
    return suffix


for i, qcd_suffix in enumerate(qcd_bins):
  qcd_sample_name = f"pythia{'Collider' if variant == 'FASER' else ''}_qcd{qcd_suffix}"

  legend = Legend(
    backgrounds_legend_x, legend_max_y - (2 + i) * legend_height,
    backgrounds_legend_x + legend_width,
    legend_max_y - (1 + i) * legend_height, "FL"
  )
  legend_description = get_nice_qcd_name(qcd_suffix)

  # if i == 0:
  #     legend = Legend(backgrounds_legend_x, legend_max_y-(2+i)*legend_height,
  #                     backgrounds_legend_x+legend_width, legend_max_y-(1+i)*legend_height, "FL")
  #     # legend_description = "QCD "+qcd_suffix
  #     legend_description = "QCD"
  # else:
  #     legend = Legend(2, 2, 3, 3, "FL")
  #     legend_description = ""

  line_color = ROOT.kGray

  samples.append(
    Sample(
      name=qcd_sample_name,
      file_path=
      f"{base_path}/{qcd_sample_name}/merged_{variant}_neutrinos_histograms.root",
      type=SampleType.background,
      cross_sections=crossSections,
      fill_color=qcd_colors[i],
      # fill_color=ROOT.kGray,
      line_color=line_color,
      fill_alpha=1.0,
      marker_size=0.0,
      legend_description=legend_description,
      custom_legend=legend,
    )
  )

  custom_stacks_order.append(qcd_sample_name)

y_label = "Events"

histograms = [
  Histogram(
    "cutFlow", "", False, True, NormalizationType.to_lumi, 1, 0, 4, 1e2, 1e17,
    "Selection", "#sum genWeight", "_" + variant
  ),
]

for hist in [
  "InitialNeutrinos", "NeutrinosHittingDetector", "nuElectron", "nuMuon",
  "nuTau"
]:
  label = "e, #mu, #tau"

  if hist == "nuElectron":
    label = "e"
  elif hist == "nuMuon":
    label = "#mu"
  elif hist == "nuTau":
    label = "#tau"

  histograms.append(
    Histogram(
      f"{hist}_logPt", "", False, True, NormalizationType.to_lumi, 1, -4, 2,
      1e-10, 1e15, "log_{10} p_{T}^{#nu_{" + label + "}} [GeV]", "Entries",
      "_" + variant
    )
  )
  histograms.append(
    Histogram(
      f"{hist}_logEnergy", "", False, True, NormalizationType.to_lumi, 10, -1, 5,
      1e-3, 1e16, "log_{10} E^{#nu_{" + label + "}} [GeV]", "Entries",
      "_" + variant
    )
  )
  histograms.append(
    Histogram(
      f"{hist}_eta", "", False, True, NormalizationType.to_lumi, 1, -5, 15,
      1e-1, 1e8, "#eta^{#nu_{" + label + "}}", "Entries", "_" + variant
    )
  )
  histograms.append(
    Histogram(
      f"{hist}_phi", "", False, True, NormalizationType.to_lumi, 1, -4, 4,
      1e-1, 1e19, "#phi^{#nu_{" + label + "}}", "Entries", "_" + variant
    )
  )
  histograms.append(
    Histogram(
      f"{hist}_pid", "", False, True, NormalizationType.to_lumi, 1, -20, 20,
      1e0, 2e8, "PID^{#nu_{" + label + "}}", "Entries", "_" + variant
    )
  )
  histograms.append(
    Histogram(
      f"{hist}_d3d", "", True, True, NormalizationType.to_lumi, 2, 1e-7, 1e3,
      1e-1, 1e17, "d_{3D}^{#nu_{" + label + "}} [m]", "Entries", "_" + variant
    )
  )
  
output_formats = ["pdf"]

plotting_options = {
  SampleType.background: "hist",
  # SampleType.background: "hist nostack e",
  SampleType.signal: "",
  SampleType.data: "",
}

canvas_size = (800, 600)
show_ratio_plots = False
ratio_limits = (0.0, 2.0)

show_cms_labels = True
lumi_label_value = luminosity / 1e3
label_y = -0.03
label_x = 0.20

label_text = "SHIFT"
beam_label = "113 GeV"

legends = {
  SampleType.signal: Legend(0, 0, 10, 10, "l"),
  SampleType.data: Legend(0, 0, 10, 10, "l"),
  SampleType.background: Legend(0, 0, 10, 10, "f"),
}
