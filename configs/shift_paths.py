base_path = "/nfs/dust/cms/user/jniedzie/shift/"
base_datacard_name = "datacard_{}"

skim = "initial"
# skim = "skimmed_allSelections"


# variant = "shift100m"
# variant = "shift300m"
# variant = "shift500m"
# variant = "shift1000m"
# variant = "cmsFT"
variant = "cms"
# variant = "faser"

if variant == "faser" or variant == "cms":
    colliderMode = True
else:
    colliderMode = False

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
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e4",
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e5",
    
    # # Z' mass scan
    # "pythia_mZprime-50_mDH-20_mDQ-1_tau-1e1",
    # "pythia_mZprime-200_mDH-20_mDQ-1_tau-1e1",
    # "pythia_mZprime-500_mDH-20_mDQ-1_tau-1e1",

    # # hD mass scan
    # "pythia_mZprime-100_mDH-15_mDQ-1_tau-1e1",
    # "pythia_mZprime-100_mDH-40_mDQ-1_tau-1e1",
    # "pythia_mZprime-100_mDH-60_mDQ-1_tau-1e1",

    # # qD mass scan
    # "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1",
    # "pythia_mZprime-100_mDH-20_mDQ-2_tau-1e1",
    # "pythia_mZprime-100_mDH-20_mDQ-5_tau-1e1",
)

if colliderMode:
    processes = [process.replace("pythia_", "pythiaCollider_") for process in processes]
    luminosity = 150 * 1e6  # fb^-1 -> nb^-1
else:
    luminosity = 150 * 1e4 # pb^-1 -> nb^-1

luminosity_err = luminosity * 0.015  # 1.5% uncertainty

reference_signal_cross_section = 1e-6  # nb

crossSections = {
    # Fixed target
    "pythia_qcd": 2.664e-06 * 1e6,  # mb -> nb
    "pythia_dy": 2.985e-08 * 1e6, # mb -> nb
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7": reference_signal_cross_section,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3": reference_signal_cross_section,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1": reference_signal_cross_section,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0": reference_signal_cross_section*1e2,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1": reference_signal_cross_section*1e3,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2": reference_signal_cross_section*1e4,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3": reference_signal_cross_section*1e5,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e4": reference_signal_cross_section*1e6,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e5": reference_signal_cross_section*1e7,
    
    # Z' mass scan
    "pythia_mZprime-50_mDH-20_mDQ-1_tau-1e1": reference_signal_cross_section*1e3,
    "pythia_mZprime-200_mDH-20_mDQ-1_tau-1e1": reference_signal_cross_section*1e3,
    "pythia_mZprime-500_mDH-20_mDQ-1_tau-1e1": reference_signal_cross_section*1e3,

    # hD mass scan
    "pythia_mZprime-100_mDH-15_mDQ-1_tau-1e1": reference_signal_cross_section*1e3,
    "pythia_mZprime-100_mDH-40_mDQ-1_tau-1e1": reference_signal_cross_section*1e3,
    "pythia_mZprime-100_mDH-60_mDQ-1_tau-1e1": reference_signal_cross_section*1e3,

    # qD mass scan
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1": reference_signal_cross_section*1e3,
    "pythia_mZprime-100_mDH-20_mDQ-2_tau-1e1": reference_signal_cross_section*1e3,
    "pythia_mZprime-100_mDH-20_mDQ-5_tau-1e1": reference_signal_cross_section*1e3,
    
    # Collider
    "pythiaCollider_qcd": 6.247e-01 * 1e6,  # mb -> nb
    "pythiaCollider_dy": 6.911e-06 * 1e6, # mb -> nb
}

nGenEvents = {
    # Fixed target
    "pythia_qcd": 999*10000,
    "pythia_dy": 1000*10000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7": 100*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3": 100*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1": 100*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0": 100*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1": 100*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2": 100*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3": 1000*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e4": 1000*1000,
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e5": 1000*1000,
    
    # Z' mass scan
    "pythia_mZprime-50_mDH-20_mDQ-1_tau-1e1": 100*1000,
    "pythia_mZprime-200_mDH-20_mDQ-1_tau-1e1": 100*1000,
    "pythia_mZprime-500_mDH-20_mDQ-1_tau-1e1": 100*1000,

    # hD mass scan
    "pythia_mZprime-100_mDH-15_mDQ-1_tau-1e1": 100*1000,
    "pythia_mZprime-100_mDH-40_mDQ-1_tau-1e1": 100*1000,
    "pythia_mZprime-100_mDH-60_mDQ-1_tau-1e1": 100*1000,

    # qD mass scan
    "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1": 100*1000,
    "pythia_mZprime-100_mDH-20_mDQ-2_tau-1e1": 100*1000,
    "pythia_mZprime-100_mDH-20_mDQ-5_tau-1e1": 100*1000,
    
    # Collider
    "pythiaCollider_qcd": 1000*100,
    "pythiaCollider_dy": 100*1000,
}

def extend_for_collider(dict):
    new_dict = {}
    
    for process, value in dict.items():
        if "Collider" in process:
            new_dict[process] = value
            continue
        
        new_process_name = process.replace("pythia_", "pythiaCollider_")
        if new_process_name not in dict:
            new_dict[new_process_name] = value
    dict = new_dict

extend_for_collider(crossSections)
extend_for_collider(nGenEvents)

histograms_path = "histograms_" + variant

if "shift" in variant:
    detectorParams = {
        "x": -1, # -1 means it will be placed on the LHC ring (based on the z coordinate)
        "y": 0,  # usually we don't want to shift the detector up and down
        "z": float(variant.replace("shift", "").replace("m", "")),
        "radius": 10,
        "maxEta": 2.4,
    }
elif variant == "faser":
    detectorParams = {
        "x": 0,
        "y": 0,
        "z": 480,
        "radius": 0.25, # equivalent sphere radius to get the same volume (and generously rounded up)
        "maxEta": 999999, # there's no hole in the detector, so we can set this to a very high value
    }
elif "cms" in variant:
    detectorParams = {
        "x": 0,
        "y": 0,
        "z": 0,
        "radius": 10,
        "maxEta": 2.4,
    }
