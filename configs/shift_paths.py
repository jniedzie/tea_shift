base_path = "/nfs/dust/cms/user/jniedzie/shift/"

skim = "initial"
# skim = "skimmed_allSelections"

processes = (
    "pythia_qcd",
    "pythia_dy",
    
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3",
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7",
)

luminosity = 150 * 1e6  # fb^-1 -> nb^-1
luminosity_err = luminosity * 0.015  # 1.5% uncertainty

reference_signal_cross_section = 1e-7  # nb

crossSections = {
    "pythia_qcd": 3.266e-06 * 1e6,  # +/- 5.400e-08 mb -> nb
    "pythia_dy": 1.518e-08 * 1e6, # +/- 2.795e-10 mb -> nb
    
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3": reference_signal_cross_section,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7": reference_signal_cross_section,
}

nGenEvents = {
    "pythia_qcd": 100000,
    "pythia_dy": 100000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3": 100000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7": 100000,
}

detectorParams = {
  "x": -1, # -1 means it will be placed on the LHC ring (based on the z coordinate)
  "y": 0,  # usually we don't want to shift the detector up and down
  "z": 300,
  "radius": 10,
}
