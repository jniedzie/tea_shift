import numpy as np

from shift_paths import detectorParams, base_path, variant

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
# inputFilePath = f"{base_path}/pythiaCollider_mDarkPhoton-30_ctau-1e1/initial/mDarkPhoton-30.0_ctau-1p00e01m_part-0.root"
inputFilePath = f"{base_path}/pythia_mDarkPhoton-30_ctau-1e1/initial/mDarkPhoton-30.0_ctau-1p00e01m_part-0.root"

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
  ("DarkPhoton", "mass",      100,  0,      100,     ""),
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
  ("InitialMuons", "boost"  ,    100,  0,      1,     ""),
  ("InitialMuonsPair", "mass"  ,    1000,  0,      100,     ""),
  ("InitialMuonsPair", "lowMass"  ,    1000,  0,      10,     ""),
  ("InitialMuonsPair", "deltaR"  ,    100,  0,      10,     ""),
  ("InitialMuonsPair", "deltaEta"  ,    200,  -10,      10,     ""),
  ("InitialMuonsPair", "deltaPhi"  ,    100,  0,      4,     ""),
  
  ("GoodInitialMuons", "pt"      ,    1000,  0,      1000,     ""),
  ("GoodInitialMuons", "energy"  ,    100,  0,      10000,     ""),
  ("GoodInitialMuons", "eta"     ,    100,  -10,    20,     ""),
  ("GoodInitialMuons", "phi"     ,    100,  -4,     4,     ""),
  ("GoodInitialMuons", "mass"    ,    100,  0,      10,     ""),
  ("GoodInitialMuons", "pid"     ,    100,  0,      10000000,     ""),
  ("GoodInitialMuons", "status"  ,    100,  0,      100,     ""),
  ("GoodInitialMuons", "boost"  ,    100,  0,      1,     ""),
  ("GoodInitialMuonsPair", "mass"  ,    1000,  0,      100,     ""),
  ("GoodInitialMuonsPair", "lowMass"  ,    1000,  0,      10,     ""),
  ("GoodInitialMuonsPair", "deltaR"  ,    100,  0,      10,     ""),
  ("GoodInitialMuonsPair", "deltaEta"  ,    400,  -20,      20,     ""),
  ("GoodInitialMuonsPair", "deltaPhi"  ,    100,  0,      4,     ""),
  
  ("GoodPtInitialMuons", "pt"      ,    1000,  0,      1000,     ""),
  ("GoodPtInitialMuons", "energy"  ,    100,  0,      10000,     ""),
  ("GoodPtInitialMuons", "eta"     ,    100,  -10,    20,     ""),
  ("GoodPtInitialMuons", "phi"     ,    100,  -4,     4,     ""),
  ("GoodPtInitialMuons", "mass"    ,    100,  0,      10,     ""),
  ("GoodPtInitialMuons", "pid"     ,    100,  0,      10000000,     ""),
  ("GoodPtInitialMuons", "status"  ,    100,  0,      100,     ""),
  ("GoodPtInitialMuons", "boost"  ,    100,  0,      1,     ""),
  ("GoodPtInitialMuonsPair", "mass"  ,    1000,  0,      100,     ""),
  ("GoodPtInitialMuonsPair", "lowMass"  ,    1000,  0,      10,     ""),
  ("GoodPtInitialMuonsPair", "deltaR"  ,    100,  0,      10,     ""),
  ("GoodPtInitialMuonsPair", "deltaEta"  ,    400,  -20,      20,     ""),
  ("GoodPtInitialMuonsPair", "deltaPhi"  ,    100,  0,      4,     ""),
  
  
  ("InitialMuonsFromDarkPhoton", "pt"      ,    1000,  0,      1000,     ""),
  ("InitialMuonsFromDarkPhoton", "energy"  ,    100,  0,      10000,     ""),
  ("InitialMuonsFromDarkPhoton", "eta"     ,    100,  -10,    20,     ""),
  
  ("MuonsHittingDetector", "pt"      ,    1000,  0,      1000,     ""),
  ("MuonsHittingDetector", "energy"  ,    200,  0,      2000,     ""),
  ("MuonsHittingDetector", "eta"     ,    100,  -10,    20,     ""),
  ("MuonsHittingDetector", "phi"     ,    100,  -4,     4,     ""),
  ("MuonsHittingDetector", "mass"    ,    100,  0,      10,     ""),
  ("MuonsHittingDetector", "pid"     ,    100,  0,      10000000,     ""),
  ("MuonsHittingDetector", "status"  ,    100,  0,      100,     ""),
  ("MuonsHittingDetector", "boost"  ,    100,  0,      1,     ""),
  
  ("MuonsHittingDetectorPair", "lowMass"  ,    1000,  0,      10,     ""),
  ("MuonsHittingDetectorPair", "deltaR"  ,    100,  0,      10,     ""),
  ("MuonsHittingDetectorPair", "deltaEta"  ,    200,  -10,      10,     ""),
  ("MuonsHittingDetectorPair", "deltaPhi"  ,    100,  0,      4,     ""),
  ("MuonsHittingDetectorPair", "mass"  ,    1000,  0,      100,     ""),
  
  ("MuonsHittingDetectorSameVertexPair", "lowMass"  ,    1000,  0,      10,     ""),
  ("MuonsHittingDetectorSameVertexPair", "deltaR"  ,    100,  0,      10,     ""),
  ("MuonsHittingDetectorSameVertexPair", "deltaEta"  ,    200,  -10,      10,     ""),
  ("MuonsHittingDetectorSameVertexPair", "deltaPhi"  ,    100,  0,      4,     ""),
  ("MuonsHittingDetectorSameVertexPair", "mass"  ,    1000,  0,      100,     ""),
  
  ("MuonsHittingDetectorSameVertexPair", "massCtauGt1cm"  ,    1000,  0,      100,     ""),
  ("MuonsHittingDetectorSameVertexPair", "massCtauGt1m"   ,    1000,  0,      100,     ""),
  ("MuonsHittingDetectorSameVertexPair", "massCtauGt10m"  ,    1000,  0,      100,     ""),
  
  ("PtMuonsHittingDetector", "pt"      ,    1000,  0,      1000,     ""),
  ("PtMuonsHittingDetector", "energy"  ,    200,  0,      2000,     ""),
  ("PtMuonsHittingDetector", "eta"     ,    100,  -10,    20,     ""),
  ("PtMuonsHittingDetector", "phi"     ,    100,  -4,     4,     ""),
  ("PtMuonsHittingDetector", "mass"    ,    100,  0,      10,     ""),
  ("PtMuonsHittingDetector", "pid"     ,    100,  0,      10000000,     ""),
  ("PtMuonsHittingDetector", "status"  ,    100,  0,      100,     ""),
  ("PtMuonsHittingDetector", "boost"  ,    100,  0,      1,     ""),
  
  ("PtMuonsHittingDetectorPair", "lowMass"  ,    1000,  0,      10,     ""),
  ("PtMuonsHittingDetectorPair", "deltaR"  ,    100,  0,      10,     ""),
  ("PtMuonsHittingDetectorPair", "deltaEta"  ,    200,  -10,      10,     ""),
  ("PtMuonsHittingDetectorPair", "deltaPhi"  ,    100,  0,      4,     ""),
  ("PtMuonsHittingDetectorPair", "mass"  ,    1000,  0,      100,     ""),
  
  ("PtMuonsHittingDetectorSameVertexPair", "lowMass"  ,    1000,  0,      10,     ""),
  ("PtMuonsHittingDetectorSameVertexPair", "deltaR"  ,    100,  0,      10,     ""),
  ("PtMuonsHittingDetectorSameVertexPair", "deltaEta"  ,    200,  -10,      10,     ""),
  ("PtMuonsHittingDetectorSameVertexPair", "deltaPhi"  ,    100,  0,      4,     ""),
  ("PtMuonsHittingDetectorSameVertexPair", "mass"  ,    1000,  0,      100,     ""),
  ("PtMuonsHittingDetectorSameVertexPair", "massCtauGt1cm"  ,    1000,  0,      100,     ""),
  ("PtMuonsHittingDetectorSameVertexPair", "massCtauGt1m"   ,    1000,  0,      100,     ""),
  ("PtMuonsHittingDetectorSameVertexPair", "massCtauGt10m"  ,    1000,  0,      100,     ""),
  
  ("Event", "nZprimes"    ,    10,  0,      10,     ""),
  ("Event", "nDarkPhotons"    ,    10,  0,      10,     ""),
  ("Event", "nDarkHadrons",    10,  0,      10,     ""),
  ("Event", "nInitialMuons",    20,  0,      20,     ""),
  ("Event", "nGoodInitialMuons",    20,  0,      20,     ""),
  ("Event", "nGoodPtInitialMuons",    20,  0,      20,     ""),
  ("Event", "nMuonsHittingDetector",    20,  0,      20,     ""),
  ("Event", "nPtMuonsHittingDetector",    20,  0,      20,     ""),
  ("Event", "count",    1,  0,      1,     ""),
)

log_bins_10 = list(np.logspace(-7, 7, 150, base=10))

irregularHistParams = (
  ("InitialMuons", "x"  ,    log_bins_10,     ""),
  ("InitialMuons", "y"  ,    log_bins_10,     ""),
  ("InitialMuons", "z"  ,    log_bins_10,     ""),
  ("InitialMuons", "d3d"  ,    log_bins_10,     ""),
  ("InitialMuons", "properCtau"  ,    log_bins_10,     ""),
  
  ("GoodInitialMuons", "x"  ,    log_bins_10,     ""),
  ("GoodInitialMuons", "y"  ,    log_bins_10,     ""),
  ("GoodInitialMuons", "z"  ,    log_bins_10,     ""),
  ("GoodInitialMuons", "d3d"  ,    log_bins_10,     ""),
  ("GoodInitialMuons", "properCtau"  ,    log_bins_10,     ""),
  
  ("GoodPtInitialMuons", "x"  ,    log_bins_10,     ""),
  ("GoodPtInitialMuons", "y"  ,    log_bins_10,     ""),
  ("GoodPtInitialMuons", "z"  ,    log_bins_10,     ""),
  ("GoodPtInitialMuons", "d3d"  ,    log_bins_10,     ""),
  ("GoodPtInitialMuons", "properCtau"  ,    log_bins_10,     ""),
  
  ("MuonsHittingDetector", "x"  ,    log_bins_10,     ""),
  ("MuonsHittingDetector", "y"  ,    log_bins_10,     ""),
  ("MuonsHittingDetector", "z"  ,    log_bins_10,     ""),
  ("MuonsHittingDetector", "d3d"  ,    log_bins_10,     ""),
  ("MuonsHittingDetector", "properCtau"  ,    log_bins_10,     ""),
  
  ("PtMuonsHittingDetector", "x"  ,    log_bins_10,     ""),
  ("PtMuonsHittingDetector", "y"  ,    log_bins_10,     ""),
  ("PtMuonsHittingDetector", "z"  ,    log_bins_10,     ""),
  ("PtMuonsHittingDetector", "d3d"  ,    log_bins_10,     ""),
  ("PtMuonsHittingDetector", "properCtau"  ,    log_bins_10,     ""),
  
  ("MuonsHittingDetectorPair", "d3d"  ,    log_bins_10,     ""),
  ("PtMuonsHittingDetectorPair", "d3d"  ,    log_bins_10,     ""),
)

# specify name of the branch containing event weights
weightsBranchName = "genWeight"

eventsTreeNames = ["Events",]
specialBranchSizes = {
  "Particle": "Event_numberP",
}

branchesToKeep = ["*"]
branchesToRemove = []
