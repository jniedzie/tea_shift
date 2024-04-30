from shift_paths import detectorParams, base_path

nEvents = -1
printEveryNevents = 100

skim = "initial"

# process = "pythia_qcd"
# process = "pythia_dy"
# process = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3"  
process = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7"

inputFilePath = f"{base_path}/{process}/merged_{skim}.root"
treeOutputFilePath = f"../skimmed_merged_{process}_{skim}.root"


# inputFilePath = "../dy_part-0.root"
# inputFilePath = "../qcd_part-0.root"
# treeOutputFilePath = "../skimmed_test.root"

# specify name of the branch containing event weights
weightsBranchName = "genWeight"

eventsTreeNames = ["Events",]
specialBranchSizes = {
  "Particle": "Event_numberP",
}

branchesToKeep = ["*"]
branchesToRemove = []
