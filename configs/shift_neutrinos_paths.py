base_path = "/data/dust/user/jniedzie/shift/"

skim = "initial"
# skim = "skimmed_allSelections"

variant = "shift160m"  # good for all signals. Use when plotting limits
# variant = "FASER"

processes = (
  # one bin QCD & DY
  # "pythia_qcd",  # ptHat > 20 GeV
  # "pythia_dy",

  # binned QCD
  # "pythia_qcd_ptHat0to1GeV",
  # "pythia_qcd_ptHat1to2GeV",
  # "pythia_qcd_ptHat2to5GeV",
  "pythia_qcd_ptHat5to10GeV",
  # "pythia_qcd_ptHat10to20GeV",
  # "pythia_qcd_ptHat20toInfGeV",

  # one bin QCD & DY for collider mode
  # "pythiaCollider_qcd",
  # "pythiaCollider_dy",

  # binned QCD for collider mode
  # "pythiaCollider_qcd_ptHat0to10GeV",
  # "pythiaCollider_qcd_ptHat10to20GeV",

  # "pythiaCollider_qcd_ptHat50to100GeV",
  # "pythiaCollider_qcd_ptHat100toInfGeV",
)

if variant == "shift160m":
  luminosity = 0.01 * 715 * 1e6  # 1% of Run 4 lumi, fb^-1 -> nb^-1
elif variant == "FASER":
  luminosity = 715 * 1e6  # Run 4 lumi, fb^-1 -> nb^-1

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

  # Collider backgrounds
  "pythiaCollider_dy": 6.911e-06 * 1e6,  # mb -> nb
  "pythiaCollider_qcd": 6.247e-01 * 1e6,  # mb -> nb (ptHat > 20 GeV)
  "pythiaCollider_qcd_ptHat0to10GeV": 2.083e+03 * 1e6,  # mb -> nb
  "pythiaCollider_qcd_ptHat0to1GeV": 2.108e+03 * 1e6,  # mb -> nb
  "pythiaCollider_qcd_ptHat1to2GeV": 1.418e+03 * 1e6,  # mb -> nb
  "pythiaCollider_qcd_ptHat2to5GeV": 5.795e+02 * 1e6,  # mb -> nb
  "pythiaCollider_qcd_ptHat5to10GeV": 5.031e+01 * 1e6,  # mb -> nb
  "pythiaCollider_qcd_ptHat10to20GeV": 6.007e+00 * 1e6,  # mb -> nb
  "pythiaCollider_qcd_ptHat20to30GeV": 4.834e-01 * 1e6,  # mb -> nb
  "pythiaCollider_qcd_ptHat30to50GeV": 1.183e-01 * 1e6,  # mb -> nb
  "pythiaCollider_qcd_ptHat50to100GeV": 1.868e-02 * 1e6,  # mb -> nb
  "pythiaCollider_qcd_ptHat100toInfGeV": 1.164e-03 * 1e6,  # mb -> nb
}

histograms_path = "neutrino_histograms_" + variant

if variant == "shift160m":
  detectorParams = {
    "x": 160,   # z
    "y": 0,     # x
    "z": 0,     # y
    "radius": 7.5,
    "length": 22,
    "maxEta": 2.4,
  }
elif variant == "FASER":
  detectorParams = {
    "x": 480,
    "y": 0,
    "z": 0,
    "radius": 0.2,
    "length": 1.5,
    "maxEta": 9999999,
  }
