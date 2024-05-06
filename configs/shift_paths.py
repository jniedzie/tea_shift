base_path = "/nfs/dust/cms/user/jniedzie/shift/"
base_datacard_name = "datacard_{}"

skim = "initial"
# skim = "skimmed_allSelections"


# variant = "shift80m"
# variant = "shift100m"
variant = "shift120m" # best for short-lived
# variant = "shift200m"
# variant = "shift250m"  # best for long-lived
# variant = "shift300m" # benchmark point
# variant = "shift350m"
# variant = "shift400m"
# variant = "shift500m"
# variant = "shift1000m"
# variant = "cmsFT"
# variant = "cms"
# variant = "faser"

if variant == "faser" or variant == "cms":
    colliderMode = True
else:
    colliderMode = False

processes = (
    # "pythia_mZprime-100_mDH-20_mDQ-10_tau-1e1",
    # "pythia_mZprime-40_mDH-20_mDQ-10_tau-1e1",
    # "pythia_mZprime-40_mDH-20_mDQ-1_tau-1em3",
    "pythia_mZprime-100_mDH-60_mDQ-1_tau-1em3",
    
    # "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7",
    # "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em3",
    # "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em1",
    # "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e0",
    # "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1",
    # "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e2",
    # "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3",
    # "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e4",
    # "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e5",
    
    # Z' mass scan
    # "pythia_mZprime-40_mDH-20_mDQ-1_tau-1e1",
    # "pythia_mZprime-50_mDH-20_mDQ-1_tau-1e1",
    # "pythia_mZprime-110_mDH-20_mDQ-1_tau-1e1",

    # # hD mass scan
    # "pythia_mZprime-100_mDH-15_mDQ-1_tau-1e1",
    # "pythia_mZprime-100_mDH-40_mDQ-1_tau-1e1",
    # "pythia_mZprime-100_mDH-60_mDQ-1_tau-1e1",

    # # qD mass scan
    # "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e1",
    # "pythia_mZprime-100_mDH-20_mDQ-2_tau-1e1",
    # "pythia_mZprime-100_mDH-20_mDQ-5_tau-1e1",
    
    
    # # other special cases
    # "pythia_mZprime-20_mDH-5_mDQ-1_tau-1e1",
    # "pythia_mZprime-100_mDH-15_mDQ-7_tau-1e1",
    
    # new points
    # "pythia_mZprime-30_mDH-15_mDQ-7_tau-1e1",
    
    # "pythia_qcd",
    # "pythia_dy",
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
    
    # # other special cases
    "pythia_mZprime-20_mDH-5_mDQ-1_tau-1e1": reference_signal_cross_section*1e3,
    "pythia_mZprime-100_mDH-20_mDQ-10_tau-1e1": reference_signal_cross_section*1e3,
    
    "pythia_mZprime-100_mDH-60_mDQ-1_tau-1em3": reference_signal_cross_section,
    
    # Collider
    "pythiaCollider_qcd": 6.247e-01 * 1e6,  # mb -> nb
    "pythiaCollider_dy": 6.911e-06 * 1e6, # mb -> nb
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

histograms_path = "histograms_" + variant

if "shift" in variant:
    detectorParams = {
        "x": float(variant.replace("shift", "").replace("m", "")),
        "y": -1, # -1 means it will be placed on the LHC ring (based on the z coordinate)
        "z": 0,  # usually we don't want to shift the detector up and down
        "radius": 7.5,
        "length": 22,
        "maxEta": 2.4,
    }
elif variant == "faser":
    detectorParams = {
        "x": 480,
        "y": 0,
        "z": 0,
        "radius": 0.1,
        "length": 1.5,
        "maxEta": 999999, # there's no hole in the detector, so we can set this to a very high value
    }
elif "cms" in variant:
    detectorParams = {
        "x": 0,
        "y": 0,
        "z": 0,
        "radius": 7.5,
        "length": 22,
        "maxEta": 2.4,
    }
