base_path = "/nfs/dust/cms/user/jniedzie/shift/"

# skim = "initial"
skim = "skimmed_allSelections"

processes = (
    "pythia_qcd",
    "pythia_dy",
    
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3",
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7",
)

luminosity = 150  # fb^-1
luminosity_err = luminosity * 0.015  # 1.5% uncertainty

reference_signal_cross_section = 10e-3  # μb

crossSections = {
    "pythia_qcd": 3.515e+01 * 1e12  ,  # +/- 2.007e-01 mb -> fb
    "pythia_dy": 1.514e-08 * 1e12, # +/- 3.324e-10 mb -> fb
    
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3": reference_signal_cross_section,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7": reference_signal_cross_section,
}

nGenEvents = {
    "pythia_qcd": 100000,
    "pythia_dy": 100000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3": 10000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7": 10000,
}
