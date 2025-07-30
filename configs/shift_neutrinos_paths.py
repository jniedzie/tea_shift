base_path = "/data/dust/user/jniedzie/shift/"

skim = "initial"
# skim = "skimmed_allSelections"

variant = "shift160m"  # good for all signals. Use when plotting limits

processes = (
  # one bin QCD
  "pythia_qcd",  # ptHat > 20 GeV

  # binned QCD
  # "pythia_qcd_ptHat0to1GeV",
  # "pythia_qcd_ptHat1to2GeV",
  # "pythia_qcd_ptHat2to5GeV",
  # "pythia_qcd_ptHat5to10GeV",
  # "pythia_qcd_ptHat10to20GeV",
  # "pythia_qcd_ptHat20toInfGeV",

  # DY
  # "pythia_dy",
)

luminosity = 0.01 * 715 * 1e6  # 1% of Run 4 lumi, fb^-1 -> nb^-1
luminosity_err = luminosity * 0.015  # 1.5% uncertainty

crossSections = {
  # Fixed target backgrounds
  "pythia_dy": 2.985e-08 * 1e6,  # mb -> nb
  "pythia_qcd": 2.664e-06 * 1e6,  # mb -> nb (ptHat > 20 GeV)
  "pythia_qcd_ptHat0to1GeV": 3.231e+01 * 1e6,  # mb -> nb
  "pythia_qcd_ptHat1to2GeV": 2.870e+01 * 1e6,  # mb -> nb
  "pythia_qcd_ptHat2to5GeV": 3.413e+00 * 1e6,  # mb -> nb
  "pythia_qcd_ptHat5to10GeV": 4.162e-02 * 1e6,  # mb -> nb
  "pythia_qcd_ptHat10to20GeV": 7.426e-04 * 1e6,  # mb -> nb
  "pythia_qcd_ptHat20toInfGeV": 2.608e-06 * 1e6,  # mb -> nb
}

histograms_path = "neutrino_histograms_" + variant

detectorParams = {
  "x": 160,
  "y": 0,
  "z": 0,
  "radius": 7.5,
  "length": 22,
  "maxEta": 2.4,
}
