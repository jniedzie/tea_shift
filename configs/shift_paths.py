base_path = "/nfs/dust/cms/user/jniedzie/shift/"
base_datacard_name = "datacard_{}"

skim = "initial"
# skim = "skimmed_allSelections"

# variant = "cms"
variant = "shift160m" # good for all signals. Use when plotting limits

# variant = "shift30m"
# variant = "shift50m"
# variant = "shift80m"
# variant = "shift100m"
# variant = "shift120m" # short-lived HV:100/20/1/X
# variant = "shift140m" # any HV:60/5/1/X
# variant = "shift200m" # long-lived DP:30/X (but short-lived also ok)
# variant = "shift250m" # long-lived HV:100/20/1/X
# variant = "shift270m"
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
    # "pythia_mDarkPhoton-5_ctau-1e1",
    # "pythia_mDarkPhoton-30_ctau-1e1",
    # "pythia_mDarkPhoton-30_ctau-1em3",
    # "pythia_mDarkPhoton-30_ctau-1e3",
    # "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em1",
    # "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1em1",
    
    # # HV: 60/20/1/X
    # "pythia_mZprime-60_mDH-20_mDQ-1_tau-1em7",
    # "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1em1",
    # "pythia_mZprime-60_mDH-20_mDQ-1_tau-1e0",
    # "pythia_mZprime-60_mDH-20_mDQ-1_tau-1e1",
    # "pythia_mZprime-60_mDH-20_mDQ-1_tau-1e3",
    
    # # HV: 60/5/1/X
    # "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em5",
    # "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em3",
    # "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em1",
    # "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e0",
    # "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e1",
    # "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e3", # exclude for CMS
    # # "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e5",
    
    # # HV: 40/15/1/X
    # "pythia_mZprime-40_mDH-15_mDQ-1_ctau-1em5",
    # "pythia_mZprime-40_mDH-15_mDQ-1_ctau-1em1",
    # "pythia_mZprime-40_mDH-15_mDQ-1_ctau-1e0",
    # "pythia_mZprime-40_mDH-15_mDQ-1_ctau-1e1",
    # "pythia_mZprime-40_mDH-15_mDQ-1_ctau-1e3",
    
    # # HV: 15/5/1/X
    # "pythia_mZprime-15_mDH-5_mDQ-1_ctau-1em5",
    # "pythia_mZprime-15_mDH-5_mDQ-1_ctau-1em1",
    # "pythia_mZprime-15_mDH-5_mDQ-1_ctau-1e0",
    # "pythia_mZprime-15_mDH-5_mDQ-1_ctau-1e1",
    # "pythia_mZprime-15_mDH-5_mDQ-1_ctau-1e2",
    # "pythia_mZprime-15_mDH-5_mDQ-1_ctau-1e3", # more stat for CMS and SHIFT ongoing
    
    # # DP: X/1e1
    # "pythia_mDarkPhoton-10_ctau-1e1",
    # "pythia_mDarkPhoton-15_ctau-1e1",
    # "pythia_mDarkPhoton-20_ctau-1e1",
    # "pythia_mDarkPhoton-30_ctau-1e1",
    # "pythia_mDarkPhoton-40_ctau-1e1",
    # "pythia_mDarkPhoton-50_ctau-1e1",
    # "pythia_mDarkPhoton-70_ctau-1e1",
    
    # # DP: 30/X
    # "pythia_mDarkPhoton-30_ctau-1em5",
    # "pythia_mDarkPhoton-30_ctau-1em3",
    # "pythia_mDarkPhoton-30_ctau-1em1",
    # "pythia_mDarkPhoton-30_ctau-1e0",
    # "pythia_mDarkPhoton-30_ctau-1e1",
    # "pythia_mDarkPhoton-30_ctau-1e3",
    
    # # DP: 15/X
    # "pythia_mDarkPhoton-15_ctau-1em5",
    # "pythia_mDarkPhoton-15_ctau-1em3",
    # "pythia_mDarkPhoton-15_ctau-1em1",
    # "pythia_mDarkPhoton-15_ctau-1e0",
    # "pythia_mDarkPhoton-15_ctau-1e1",
    # # "pythia_mDarkPhoton-15_ctau-1e2", # also in mass scan
    # # "pythia_mDarkPhoton-15_ctau-1e3",
    
    # # # # DP grid scan    
    # # # DP: X/1em5
    # "pythia_mDarkPhoton-10_ctau-1em5",
    # "pythia_mDarkPhoton-20_ctau-1em5",
    # "pythia_mDarkPhoton-40_ctau-1em5",
    # "pythia_mDarkPhoton-50_ctau-1em5",
    # "pythia_mDarkPhoton-70_ctau-1em5",
    # "pythia_mDarkPhoton-70_ctau-1em5",

    # # # # DP: X/1em1
    # "pythia_mDarkPhoton-10_ctau-1em1",
    # "pythia_mDarkPhoton-20_ctau-1em1",
    # "pythia_mDarkPhoton-40_ctau-1em1",
    # "pythia_mDarkPhoton-50_ctau-1em1",
    # "pythia_mDarkPhoton-60_ctau-1em1",
    # "pythia_mDarkPhoton-70_ctau-1em1",

    # # # # DP: X/1e0
    # "pythia_mDarkPhoton-10_ctau-1e0",
    # "pythia_mDarkPhoton-20_ctau-1e0",
    # "pythia_mDarkPhoton-40_ctau-1e0",
    # "pythia_mDarkPhoton-50_ctau-1e0",
    # "pythia_mDarkPhoton-60_ctau-1e0",
    # "pythia_mDarkPhoton-70_ctau-1e0",

    # # # # # DP: X/1e3
    # "pythia_mDarkPhoton-10_ctau-1e3",
    # "pythia_mDarkPhoton-20_ctau-1e3",
    # "pythia_mDarkPhoton-40_ctau-1e3",
    # "pythia_mDarkPhoton-50_ctau-1e3",
    # "pythia_mDarkPhoton-60_ctau-1e3",
    # "pythia_mDarkPhoton-70_ctau-1e3",
    
    # # DP: X/1e2
    # "pythia_mDarkPhoton-15_ctau-1e2", # also in ctau scan
    # "pythia_mDarkPhoton-20_ctau-1e2",
    # "pythia_mDarkPhoton-40_ctau-1e2",
    # "pythia_mDarkPhoton-50_ctau-1e2",
    # "pythia_mDarkPhoton-70_ctau-1e2",

    # DP: X/1e4
    # "pythia_mDarkPhoton-10_ctau-1e4", # TODO: make hists for shift
    # "pythia_mDarkPhoton-15_ctau-1e4",
    # "pythia_mDarkPhoton-20_ctau-1e4",
    # "pythia_mDarkPhoton-40_ctau-1e4",
    # "pythia_mDarkPhoton-50_ctau-1e4",
    # "pythia_mDarkPhoton-60_ctau-1e4",
    # "pythia_mDarkPhoton-70_ctau-1e4",

    # old QCD
    # "pythia_qcd_ptHat50GeV",
    # "pythia_qcd", # ptHat > 20 GeV
    # "pythia_qcd_ptHat10GeV",
    # "pythia_qcd_ptHat5GeV",
    # "pythia_qcd_ptHat1GeV",
    # "pythia_qcd_ptHat0GeV",
    
    # new backgrounds
    # "pythia_dy",
    
    # for SHIFT
    "pythia_qcd_ptHat0to1GeV",
    "pythia_qcd_ptHat1to2GeV",
    "pythia_qcd_ptHat2to5GeV",
    # "pythia_qcd_ptHat5to10GeV",
    "pythia_qcd_ptHat10to20GeV",
    "pythia_qcd_ptHat20toInfGeV",
    
    # for CMS
    # "pythia_qcd_ptHat0to1GeV",
    # "pythia_qcd_ptHat1to2GeV",
    # "pythia_qcd_ptHat2to5GeV",
    # "pythia_qcd_ptHat5to10GeV",
    # "pythia_qcd_ptHat10to20GeV",
    # "pythia_qcd_ptHat20to50GeV",
    # "pythia_qcd_ptHat50to100GeV",
    # "pythia_qcd_ptHat100toInfGeV",
)

# base_lumi = 150 * 1e6  # fb^-1 -> nb^-1, Run 2
base_lumi = 715 * 1e6  # fb^-1 -> nb^-1, Run 4
reference_signal_cross_section = 1e-6  # nb
collider_cross_section_scale = 1e3

if colliderMode:
    processes = [process.replace("pythia_", "pythiaCollider_") for process in processes]
    luminosity = base_lumi
    reference_signal_cross_section *= collider_cross_section_scale
else:
    luminosity = 0.01 * base_lumi  # 1% of nominal luminosity for fixed-target mode

if variant == "lhcb":
    luminosity /= 25 # LHCb collects 25 times less data than CMS

luminosity_err = luminosity * 0.015  # 1.5% uncertainty


crossSections = {
    # Fixed target backgrounds
    "pythia_dy": 2.985e-08 * 1e6, # mb -> nb
    
    "pythia_qcd": 2.664e-06 * 1e6,  # mb -> nb (ptHat > 20 GeV)
    "pythia_qcd_ptHat0to1GeV": 3.231e+01 * 1e6,  # mb -> nb
    "pythia_qcd_ptHat1to2GeV": 2.870e+01 * 1e6,  # mb -> nb
    "pythia_qcd_ptHat2to5GeV": 3.413e+00 * 1e6,  # mb -> nb
    "pythia_qcd_ptHat5to10GeV": 4.162e-02 * 1e6,  # mb -> nb
    "pythia_qcd_ptHat10to20GeV": 7.426e-04 * 1e6,  # mb -> nb
    "pythia_qcd_ptHat20toInfGeV": 2.608e-06 * 1e6,  # mb -> nb
    
    
    # Collider backgrounds
    "pythiaCollider_dy": 6.911e-06 * 1e6, # mb -> nb
    
    "pythiaCollider_qcd": 6.247e-01 * 1e6,  # mb -> nb (ptHat > 20 GeV)
    "pythiaCollider_qcd_ptHat0to1GeV": 2.108e+03 * 1e6,  # mb -> nb
    "pythiaCollider_qcd_ptHat1to2GeV": 1.418e+03 * 1e6,  # mb -> nb
    "pythiaCollider_qcd_ptHat2to5GeV": 5.795e+02 * 1e6,  # mb -> nb
    "pythiaCollider_qcd_ptHat5to10GeV": 5.031e+01 * 1e6,  # mb -> nb
    "pythiaCollider_qcd_ptHat10to20GeV": 6.007e+00 * 1e6,  # mb -> nb
    "pythiaCollider_qcd_ptHat20to50GeV": 5.819e-01 * 1e6,  # mb -> nb
    "pythiaCollider_qcd_ptHat50to100GeV": 1.868e-02 * 1e6,  # mb -> nb
    "pythiaCollider_qcd_ptHat100toInfGeV": 1.164e-03 * 1e6,  # mb -> nb
    
    # DP: X/1e1
    "pythia_mDarkPhoton-5_ctau-1e1": reference_signal_cross_section*1e5,
    "pythia_mDarkPhoton-10_ctau-1e1": reference_signal_cross_section*1e5,
    "pythia_mDarkPhoton-15_ctau-1e1": reference_signal_cross_section*1e4,
    "pythia_mDarkPhoton-20_ctau-1e1": reference_signal_cross_section*1e4,
    "pythia_mDarkPhoton-40_ctau-1e1": reference_signal_cross_section*1e3,
    "pythia_mDarkPhoton-50_ctau-1e1": reference_signal_cross_section*1e3,
    "pythia_mDarkPhoton-70_ctau-1e1": reference_signal_cross_section*1e2,
    
    # DP: 30/X
    "pythia_mDarkPhoton-30_ctau-1em5": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-30_ctau-1em3": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-30_ctau-1em1": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-30_ctau-1e0": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-30_ctau-1e1": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-30_ctau-1e3": reference_signal_cross_section*1e5,
    "pythia_mDarkPhoton-30_ctau-1e5": reference_signal_cross_section*1e6,
    
    # DP: 15/X
    "pythia_mDarkPhoton-15_ctau-1em3": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-15_ctau-1e2": reference_signal_cross_section*1e3,
    "pythia_mDarkPhoton-15_ctau-1e5": reference_signal_cross_section*1e6,
    
    # HV: 60/5/1/X
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em5": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em3": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1em1": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e0": reference_signal_cross_section*1e2,
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e1": reference_signal_cross_section*1e3,
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e3": reference_signal_cross_section*1e7,
    "pythia_mZprime-60_mDH-5_mDQ-1_ctau-1e5": reference_signal_cross_section*1e9, 
    
    # HV: 60/20/1/X
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1em7": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1em5": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1em3": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1em1": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1e0": reference_signal_cross_section,
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1e1": reference_signal_cross_section*1e3,
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1e3": reference_signal_cross_section*1e5,
    "pythia_mZprime-60_mDH-20_mDQ-1_ctau-1e5": reference_signal_cross_section*1e7, 
    
    # # HV: 40/15/1/X
    "pythia_mZprime-40_mDH-15_mDQ-1_ctau-1em5": reference_signal_cross_section,
    "pythia_mZprime-40_mDH-15_mDQ-1_ctau-1em1": reference_signal_cross_section,
    "pythia_mZprime-40_mDH-15_mDQ-1_ctau-1e0": reference_signal_cross_section*1e2,
    "pythia_mZprime-40_mDH-15_mDQ-1_ctau-1e1": reference_signal_cross_section*1e3,
    "pythia_mZprime-40_mDH-15_mDQ-1_ctau-1e3": reference_signal_cross_section*1e3,
    
    # # HV: 15/5/1/X
    "pythia_mZprime-15_mDH-5_mDQ-1_ctau-1em5": reference_signal_cross_section*1e3,
    "pythia_mZprime-15_mDH-5_mDQ-1_ctau-1em1": reference_signal_cross_section*1e3,
    "pythia_mZprime-15_mDH-5_mDQ-1_ctau-1e0": reference_signal_cross_section*1e3,
    "pythia_mZprime-15_mDH-5_mDQ-1_ctau-1e1": reference_signal_cross_section*1e5,
    "pythia_mZprime-15_mDH-5_mDQ-1_ctau-1e2": reference_signal_cross_section*1e6,
    "pythia_mZprime-15_mDH-5_mDQ-1_ctau-1e3": reference_signal_cross_section*1e7,
    
    # for old (bad) names
    "pythia_mZprime-60_mDH-20_mDQ-1_tau-1em7": reference_signal_cross_section*1e2,
    "pythia_mZprime-60_mDH-20_mDQ-1_tau-1em1": reference_signal_cross_section*1e2,
    "pythia_mZprime-60_mDH-20_mDQ-1_tau-1e0": reference_signal_cross_section*1e2,
    "pythia_mZprime-60_mDH-20_mDQ-1_tau-1e1": reference_signal_cross_section*1e3,
    "pythia_mZprime-60_mDH-20_mDQ-1_tau-1e3": reference_signal_cross_section*1e5,
    
    # DP grid scan
    # DP: 70/X
    "pythia_mDarkPhoton-70_ctau-1em5": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-70_ctau-1em1": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-70_ctau-1e0": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-70_ctau-1e3": reference_signal_cross_section*1e5,

    # DP: 10/X
    "pythia_mDarkPhoton-10_ctau-1em5": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-10_ctau-1em1": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-10_ctau-1e0": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-10_ctau-1e3": reference_signal_cross_section*1e5,

    # DP: X/1e3
    "pythia_mDarkPhoton-10_ctau-1e3": reference_signal_cross_section*1e5,
    "pythia_mDarkPhoton-15_ctau-1e3": reference_signal_cross_section*1e4,
    "pythia_mDarkPhoton-20_ctau-1e3": reference_signal_cross_section*1e4,
    "pythia_mDarkPhoton-50_ctau-1e3": reference_signal_cross_section*1e3,
    "pythia_mDarkPhoton-70_ctau-1e3": reference_signal_cross_section*1e2,

    # DP: X/1em5
    "pythia_mDarkPhoton-10_ctau-1em5": reference_signal_cross_section*1e4,
    "pythia_mDarkPhoton-15_ctau-1em5": reference_signal_cross_section*1e3,
    "pythia_mDarkPhoton-20_ctau-1em5": reference_signal_cross_section*1e3,
    "pythia_mDarkPhoton-50_ctau-1em5": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-70_ctau-1em5": reference_signal_cross_section*1e1,
    
    # DP: X/1e0
    "pythia_mDarkPhoton-15_ctau-1e0": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-20_ctau-1e0": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-50_ctau-1e0": reference_signal_cross_section*1e2,

    # DP: X/1em1
    "pythia_mDarkPhoton-15_ctau-1em1": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-20_ctau-1em1": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-50_ctau-1em1": reference_signal_cross_section*1e2,
    
    # DP: X/1e4
    "pythia_mDarkPhoton-10_ctau-1e4": reference_signal_cross_section*1e6, 
    "pythia_mDarkPhoton-15_ctau-1e4": reference_signal_cross_section*1e6, 
    "pythia_mDarkPhoton-20_ctau-1e4": reference_signal_cross_section*1e6, 
    "pythia_mDarkPhoton-40_ctau-1e4": reference_signal_cross_section*1e6, 
    "pythia_mDarkPhoton-50_ctau-1e4": reference_signal_cross_section*1e6, 
    "pythia_mDarkPhoton-60_ctau-1e4": reference_signal_cross_section*1e6, 
    "pythia_mDarkPhoton-70_ctau-1e4": reference_signal_cross_section*1e6, 
    
    # DP: X/1e2
    "pythia_mDarkPhoton-10_ctau-1e2": reference_signal_cross_section*1e7,
    "pythia_mDarkPhoton-20_ctau-1e2": reference_signal_cross_section*1e3,
    "pythia_mDarkPhoton-40_ctau-1e2": reference_signal_cross_section*1e3,
    "pythia_mDarkPhoton-50_ctau-1e2": reference_signal_cross_section*1e3,
    "pythia_mDarkPhoton-70_ctau-1e2": reference_signal_cross_section*1e3,
    
    # DP: 40/X
    "pythia_mDarkPhoton-40_ctau-1em5": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-40_ctau-1em1": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-40_ctau-1e0": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-40_ctau-1e3": reference_signal_cross_section*1e5,

    # DP: 60/X
    "pythia_mDarkPhoton-60_ctau-1em1": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-60_ctau-1e0": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-60_ctau-1e1": reference_signal_cross_section*1e2,
    "pythia_mDarkPhoton-60_ctau-1e2": reference_signal_cross_section*1e3,
    "pythia_mDarkPhoton-60_ctau-1e3": reference_signal_cross_section*1e5,
}

signalCrossSectionFixedTargetDP = {
    # mb -> nb
    5: 2.327e-08 * 1e6,
    10: 2.109e-06 * 1e6,
    15: 7.820e-07 * 1e6,
    20: 1.949e-07 * 1e6,
    30: 1.816e-08 * 1e6,
    40: 2.320e-09 * 1e6,
    50: 3.697e-10 * 1e6,
    70: 3.555e-11 * 1e6,
}

signalCrossSectionFixedTargetDP_smallCoupling = {
    # mb -> nb
    # vd=ad=0.06, vu=au=0.03
    # 10: 1.943e-08 * 1e6,
    # 30: 1.732e-10 * 1e6,
    # 70: 1.200e-13 * 1e6,
    
    # vd=ad=0.04, vu=au=0.02
    5: 3.291e-11 * 1e6,
    10: 8.744e-09 * 1e6,
    15: 3.313e-09 * 1e6,
    20: 8.218e-10 * 1e6,
    30: 7.550e-11 * 1e6,
    40: 8.211e-12 * 1e6,
    50: 1.003e-12 * 1e6,
    60 : 1.689e-13 * 1e6,
    70: 5.343e-14 * 1e6,
}

signalCrossSectionColliderDP = {
    # mb -> nb
    5: 4.197e-06 * 1e6,
    10: 2.306e-04 * 1e6,
    20: 8.873e-05 * 1e6,
    30: 3.179e-05 * 1e6,
    40: 1.557e-05 * 1e6,
    50: 8.208e-06 * 1e6,
    70: 3.242e-06 * 1e6,
}

signalCrossSectionColliderDP_smallCoupling = {
    # mb -> nb
    # vd=ad=0.06, vu=au=0.03
    # 10: 2.297e-06 * 1e6,
    # 30: 3.526e-07 * 1e6,
    # 70: 3.577e-08 * 1e6,
    
    # vd=ad=0.04, vu=au=0.02
    10: 1.009e-06 * 1e6,
    15: 8.334e-07 * 1e6,
    20: 4.273e-07 * 1e6,
    30: 1.585e-07 * 1e6,
    40: 7.503e-08 * 1e6,
    50: 4.072e-08 * 1e6,
    60: 2.439e-08 * 1e6,
    70: 1.556e-08 * 1e6,
}

signalCrossSectionFixedTargetHV = {
    # vs. mZ'
    # mb -> nb
    15: 1.232e-08 * 1e6,
    20: 2.329e-09 * 1e6,
    30: 1.485e-10 * 1e6,
    40: 1.299e-11 * 1e6,
    60: 9.167e-14 * 1e6,
}

signalCrossSectionColliderHV = {
    # vs. mZ'
    # mb -> nb
    15: 2.726e-06 * 1e6,
    20: 1.040e-06 * 1e6,
    30: 2.666e-07 * 1e6,
    40: 9.818e-08 * 1e6,
    60: 2.194e-08 * 1e6,
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
