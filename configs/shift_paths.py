base_path = "/nfs/dust/cms/user/jniedzie/shift/"
base_datacard_name = "datacard_{}"

skim = "initial"
# skim = "skimmed_allSelections"

variant = "cms"
# variant = "shift160m" # good for all signals

# variant = "shift80m"
# variant = "shift100m"
# variant = "shift120m" # short-lived HV:100/20/1/X
# variant = "shift140m" # any HV:60/5/1/X
# variant = "shift200m" # long-lived DP:30/X (but short-lived also ok)
# variant = "shift250m" # long-lived HV:100/20/1/X
# variant = "shift290m"
# variant = "shift300m"
# variant = "shift310m"
# variant = "shift350m"
# variant = "shift400m"
# variant = "shift500m"
# variant = "shift1000m"
# variant = "cmsFT"
# variant = "faser"
# variant = "lhcb"
# variant = "cmsPT"

if variant == "faser" or variant == "cms" or variant == "cmsPT":
    colliderMode = True
else:
    colliderMode = False

processes = (
    # benchmark points:
    "pythia_mDarkPhoton-5_ctau-1e1",
    "pythia_mDarkPhoton-30_ctau-1e1",
    "pythia_mDarkPhoton-30_ctau-1em3",
    "pythia_mDarkPhoton-30_ctau-1e3",
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em1",
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1em1",
    
    # DP: X/1e1
    # "pythia_mDarkPhoton-5_ctau-1e1",
    # "pythia_mDarkPhoton-10_ctau-1e1",
    # "pythia_mDarkPhoton-15_ctau-1e1",
    # "pythia_mDarkPhoton-20_ctau-1e1",
    # "pythia_mDarkPhoton-30_ctau-1e1",
    # "pythia_mDarkPhoton-40_ctau-1e1",
    # "pythia_mDarkPhoton-50_ctau-1e1",
    # "pythia_mDarkPhoton-70_ctau-1e1",
    
    # DP: 30/X
    # "pythia_mDarkPhoton-30_ctau-1em5",
    # "pythia_mDarkPhoton-30_ctau-1em3",
    # "pythia_mDarkPhoton-30_ctau-1em1",
    # "pythia_mDarkPhoton-30_ctau-1e0",
    # "pythia_mDarkPhoton-30_ctau-1e1",
    # "pythia_mDarkPhoton-30_ctau-1e3",
    # "pythia_mDarkPhoton-30_ctau-1e5",
    
    # HV: 60/20/1/X
    # "pythia_mZprime-60_mDH-20_mDQ-1_tau-1em7",
    # "pythia_mZprime-60_mDH-20_mDQ-1_tau-1em1",
    # "pythia_mZprime-60_mDH-20_mDQ-1_tau-1e0",
    # "pythia_mZprime-60_mDH-20_mDQ-1_tau-1e1",
    # "pythia_mZprime-60_mDH-20_mDQ-1_tau-1e3",
    
    # HV: 60/5/1/X
    # "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em5",
    # "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em3",
    # "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em1",
    # "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e0",
    # "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e1",
    # "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e3",
    # "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e5",
     
    "pythia_qcd",
    "pythia_dy",
)

# base_lumi = 150 * 1e6  # fb^-1 -> nb^-1, Run 2
base_lumi = 715 * 1e6  # fb^-1 -> nb^-1, Run 4

if colliderMode:
    processes = [process.replace("pythia_", "pythiaCollider_") for process in processes]
    luminosity = base_lumi
else:
    luminosity = 0.01 * base_lumi  # 1% of nominal luminosity for fixed-target mode

if variant == "lhcb":
    luminosity /= 25 # LHCb collects 25 times less data than CMS

luminosity_err = luminosity * 0.015  # 1.5% uncertainty

reference_signal_cross_section = 1e-6  # nb

crossSections = {
    # Fixed target backgrounds
    "pythia_qcd": 2.664e-06 * 1e6,  # mb -> nb
    "pythia_dy": 2.985e-08 * 1e6, # mb -> nb
    
    # Collider backgrounds
    "pythiaCollider_qcd": 6.247e-01 * 1e6,  # mb -> nb
    "pythiaCollider_dy": 6.911e-06 * 1e6, # mb -> nb
    
    # DP: X/1e1
    "pythia_mDarkPhoton-5_ctau-1e1": reference_signal_cross_section*1e5,
    "pythia_mDarkPhoton-10_ctau-1e1": reference_signal_cross_section*1e7,
    "pythia_mDarkPhoton-15_ctau-1e1": reference_signal_cross_section*1e4,
    "pythia_mDarkPhoton-20_ctau-1e1": reference_signal_cross_section*1e5,
    "pythia_mDarkPhoton-40_ctau-1e1": reference_signal_cross_section*1e4,
    "pythia_mDarkPhoton-50_ctau-1e1": reference_signal_cross_section*1e4,
    "pythia_mDarkPhoton-70_ctau-1e1": reference_signal_cross_section*1e3,
    
    # DP: 30/X
    "pythia_mDarkPhoton-30_ctau-1em5": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-30_ctau-1em3": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-30_ctau-1em1": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-30_ctau-1e0": reference_signal_cross_section*1e3,
    "pythia_mDarkPhoton-30_ctau-1e1": reference_signal_cross_section*1e4,
    "pythia_mDarkPhoton-30_ctau-1e3": reference_signal_cross_section*1e5,
    "pythia_mDarkPhoton-30_ctau-1e5": reference_signal_cross_section*1e6,
    
    # HV: 60/5/1/X
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em5": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em3": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em1": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e0": reference_signal_cross_section*1e2,
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e1": reference_signal_cross_section*1e3,
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e3": reference_signal_cross_section*1e5,
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e5": reference_signal_cross_section*1e7, 
    
    # HV: 60/20/1/X
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1em7": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1em5": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1em3": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1em1": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1e0": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1e1": reference_signal_cross_section*1e3,
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1e3": reference_signal_cross_section*1e5,
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1e5": reference_signal_cross_section*1e7, 
    
    # for old (bad) names
    "pythia_mZprime-60_mDH-20_mDQ-1_tau-1em7": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-20_mDQ-1_tau-1em5": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-20_mDQ-1_tau-1em3": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-20_mDQ-1_tau-1em1": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-20_mDQ-1_tau-1e0": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-20_mDQ-1_tau-1e1": reference_signal_cross_section*1e3,
    "pythia_mZprime-60_mDH-20_mDQ-1_tau-1e3": reference_signal_cross_section*1e5,
    "pythia_mZprime-60_mDH-20_mDQ-1_tau-1e5": reference_signal_cross_section*1e7, 
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
elif variant == "lhcb":
    detectorParams = {
        "minLength": 12.5,
        "maxLength": 22.0,
        "minEta": 2.0,
        "maxEta": 5.0,
    }
