from shift_paths import detectorParams, base_path

## specify how many events to run on (and how often to print current event number)
nEvents = -1
printEveryNevents = 100

mZprime = 60
mDH = 5
mDQ = 1
ctau = "1em1"

# inputFilePath = f"{base_path}/pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7/initial/mZprime-100GeV_mDarkHadron-20GeV_mDarkQuark-1GeV_lifetime-1p00em07m_nEvents-1000_part-0.root"
# inputFilePath = f"{base_path}/pythia_mZprime-{mZprime}_mDH-{mDH}_mDQ-{mDQ}_ctau-{ctau}/initial/mZprime-{mZprime}GeV_mDH-{mDH}GeV_mDQ-{mDQ}GeV_ctau-1p00em01m_part-0.root"
# inputFilePath = f"{base_path}/pythiaCollider_qcd/initial/qcd_part-0.root"
# inputFilePath = f"{base_path}/pythia_qcd/initial/qcd_part-0.root"
# inputFilePath = f"{base_path}/pythia_dy/initial/dy_part-0.root"
# inputFilePath = "../mDarkPhoton-25.0_part-0.root"
inputFilePath = f"{base_path}/pythiaCollider_mDarkPhoton-30/initial/mDarkPhoton-30.0_part-1.root"

treeOutputFilePath = "../trees_signal.root"
histogramsOutputFilePath = "../histograms_signal.root"

defaultHistParams = []

histParams = (
#    name                 bins  xmin    xmax    dir
  ("Zprime", "pt"  ,      100,  0,      1000,     ""),
  ("Zprime", "eta" ,      100,  -10,    20,     ""),
  ("Zprime", "phi" ,      100,  -4,     4,     ""),
  ("Zprime", "mass",      100,  0,      500,     ""),
  ("Zprime", "pid"  ,     100,  0,      10000000,     ""),
  ("Zprime", "status",    100,  0,      100,     ""),
  
  ("DarkPhoton", "pt"  ,      100,  0,      1000,     ""),
  ("DarkPhoton", "eta" ,      100,  -10,    20,     ""),
  ("DarkPhoton", "phi" ,      100,  -4,     4,     ""),
  ("DarkPhoton", "mass",      100,  0,      500,     ""),
  ("DarkPhoton", "pid"  ,     100,  0,      10000000,     ""),
  ("DarkPhoton", "status",    100,  0,      100,     ""),
  
  ("DarkHadron", "pt"  ,      200,  0,      200,     ""),
  ("DarkHadron", "eta" ,      100,  -10,    20,     ""),
  ("DarkHadron", "phi" ,      100,  -4,     4,     ""),
  ("DarkHadron", "mass",      100,  0,      10,     ""),
  ("DarkHadron", "pid"  ,     100,  0,      10000000,     ""),
  ("DarkHadron", "status",    100,  0,      100,     ""),
  
  ("InitialMuons", "pt"      ,    1000,  0,      1000,     ""),
  ("InitialMuons", "energy"  ,    100,  0,      10000,     ""),
  ("InitialMuons", "eta"     ,    100,  -10,    20,     ""),
  ("InitialMuons", "phi"     ,    100,  -4,     4,     ""),
  ("InitialMuons", "mass"    ,    100,  0,      10,     ""),
  ("InitialMuons", "pid"     ,    100,  0,      10000000,     ""),
  ("InitialMuons", "status"  ,    100,  0,      100,     ""),
  ("InitialMuons", "x"  ,    100,  -10000000,      10000000,     ""),
  ("InitialMuons", "y"  ,    100,  -10000000,      10000000,     ""),
  ("InitialMuons", "z"  ,    100,  -1000000000,      1000000000,     ""),
  ("InitialMuonsPair", "mass"  ,    1000,  0,      100,     ""),
  ("InitialMuonsPair", "lowMass"  ,    1000,  0,      10,     ""),
  ("InitialMuonsPair", "deltaR"  ,    100,  0,      10,     ""),
  
  ("InitialMuonsFromDarkPhoton", "pt"      ,    1000,  0,      1000,     ""),
  ("InitialMuonsFromDarkPhoton", "energy"  ,    100,  0,      10000,     ""),
  ("InitialMuonsFromDarkPhoton", "eta"     ,    100,  -10,    20,     ""),
  
  ("MuonsHittingDetector", "pt"      ,    1000,  0,      1000,     ""),
  ("MuonsHittingDetector", "energy"  ,    100,  0,      10000,     ""),
  ("MuonsHittingDetector", "eta"     ,    100,  -10,    20,     ""),
  ("MuonsHittingDetector", "phi"     ,    100,  -4,     4,     ""),
  ("MuonsHittingDetector", "mass"    ,    100,  0,      10,     ""),
  ("MuonsHittingDetector", "pid"     ,    100,  0,      10000000,     ""),
  ("MuonsHittingDetector", "status"  ,    100,  0,      100,     ""),
  ("MuonsHittingDetector", "x"  ,    100,  -10000000,      10000000,     ""),
  ("MuonsHittingDetector", "y"  ,    100,  -10000000,      10000000,     ""),
  ("MuonsHittingDetector", "z"  ,    100,  -1000000000,      1000000000,     ""),
  ("MuonsHittingDetectorPair", "mass"  ,    1000,  0,      100,     ""),
  ("MuonsHittingDetectorPair", "lowMass"  ,    1000,  0,      10,     ""),
  ("MuonsHittingDetectorPair", "deltaR"  ,    100,  0,      10,     ""),
  
  ("Event", "nZprimes"    ,    10,  0,      10,     ""),
  ("Event", "nDarkPhotons"    ,    10,  0,      10,     ""),
  ("Event", "nDarkHadrons",    10,  0,      10,     ""),
  ("Event", "nInitialMuons",    20,  0,      20,     ""),
  ("Event", "nMuonsHittingDetector",    20,  0,      20,     ""),
  ("Event", "count",    1,  0,      1,     ""),
)

# specify name of the branch containing event weights
weightsBranchName = "genWeight"

eventsTreeNames = ["Events",]
specialBranchSizes = {
  "Particle": "Event_numberP",
}

branchesToKeep = ["*"]
branchesToRemove = []
