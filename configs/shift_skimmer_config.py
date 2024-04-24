## specify how many events to run on (and how often to print current event number)
nEvents = -1
printEveryNevents = 100

base_path = "/nfs/dust/cms/user/jniedzie/shift"

mZprime = 100
mDarkHadron = 20
mDarkQuark = 1

input_skim = "initial"

process = f"pythia_mZprime-{mZprime}_mDH-{mDarkHadron}_mDQ-{mDarkQuark}_tau-1e3"
# process = f"pythia_mZprime-{mZprime}_mDH-{mDarkHadron}_mDQ-{mDarkQuark}_tau-1em7"
# process = "pythia_qcd"
# process = "pythia_dy"

# inputFilePath = "./mZprime-100GeV_mDarkHadron-20GeV_mDarkQuark-1GeV_lifetime-1p00em07m_nEvents-1000_part-0.root"
# inputFilePath = "./qcd_part-0.root"
treeOutputFilePath = "./skimmed_test.root"

inputFilePath = f"{base_path}/{process}/merged_{input_skim}.root"
# inputFilePath = f"{base_path}/{process}/mZprime-{mZprime}GeV_mDarkHadron-{mDarkHadron}GeV_mDarkQuark-{mDarkQuark}GeV_lifetime-1p00em07m_nEvents-100_part-0.root"
# treeOutputFilePath = f"../skimmed_merged_{process}.root"

# specify name of the branch containing event weights
weightsBranchName = "genWeight"

eventsTreeNames = ["Events",]
specialBranchSizes = {
  "Particle": "Event_numberP",
}
  
detectorXshift = 10

detectorParams = {
  "x": -1, # -1 means it will be placed on the LHC ring (based on the z coordinate)
  "y": 0,  # usually we don't want to shift the detector up and down
  "z": 300,
  "radius": 10,
}

branchesToKeep = ["*"]
branchesToRemove = []
