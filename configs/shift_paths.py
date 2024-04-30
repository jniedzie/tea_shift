base_path = "/nfs/dust/cms/user/jniedzie/shift/"

skim = "initial"
# skim = "skimmed_allSelections"

processes = (
    "pythia_qcd",
    "pythia_dy",
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7",
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3",
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1",
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0",
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1",
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2",
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3",
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e5",
)

luminosity = 150 * 1e6  # fb^-1 -> nb^-1
luminosity_err = luminosity * 0.015  # 1.5% uncertainty

reference_signal_cross_section = 1e-6  # nb

crossSections = {
    "pythia_qcd": 2.664e-06 * 1e6,  # mb -> nb
    "pythia_dy": 2.985e-08 * 1e6, # mb -> nb
    
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7": reference_signal_cross_section,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3": reference_signal_cross_section,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1": reference_signal_cross_section,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0": reference_signal_cross_section,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1": reference_signal_cross_section,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2": reference_signal_cross_section,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3": reference_signal_cross_section,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e5": reference_signal_cross_section,
}

nGenEvents = {
    "pythia_qcd": 990*1000,
    "pythia_dy": 993*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7": 100*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3": 100*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1": 100*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0": 100*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1": 100*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2": 100*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3": 100*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e5": 100*1000,
}

# histograms_path = "histograms_z-300m_onLHC"
# histograms_path = "histograms_faser"
# histograms_path = "histograms_cmsFT"
histograms_path = "histograms_atlasFT"

# # SHIFT
# detectorParams = {
#   "x": -1, # -1 means it will be placed on the LHC ring (based on the z coordinate)
#   "y": 0,  # usually we don't want to shift the detector up and down
#   "z": 300,
#   "radius": 10,
# }

# FASER
# detectorParams = {
#   "x": 0,
#   "y": 0,
#   "z": 480,
#   "radius": 0.25, # equivalent sphere radius to get the same volume (and generously rounded up)
# }

# CMS
# detectorParams = {
#   "x": 0,
#   "y": 0,
#   "z": 0,
#   "radius": 10,
# }

# # ATLAS
detectorParams = {
  "x": 0,
  "y": 0,
  "z": 0,
  "radius": 18,
}
