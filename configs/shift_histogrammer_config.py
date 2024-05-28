import numpy as np

import sys
import os

# Add the directory containing shift_paths.py to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

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
# inputFilePath = f"{base_path}/pythiaCollider_dy/initial/dy_part-3.root"
# inputFilePath = f"{base_path}/pythia_dy/initial/dy_part-0.root"
# inputFilePath = "../mDarkPhoton-25.0_part-0.root"
# inputFilePath = f"{base_path}/pythiaCollider_mDarkPhoton-30_ctau-1e1/initial/mDarkPhoton-30.0_ctau-1p00e01m_part-0.root"
# inputFilePath = f"{base_path}/pythia_mDarkPhoton-30_ctau-1e1/initial/mDarkPhoton-30.0_ctau-1p00e01m_part-0.root"

inputFilePath = "../utils/example_signal.root"

# inputFilePath = f"{base_path}/pythia_mZprime-{mZprime}_mDH-{mDH}_mDQ-{mDQ}_ctau-{ctau}/initial/mZprime-{mZprime}GeV_mDH-{mDH}GeV_mDQ-{mDQ}GeV_ctau-1p00em01m_part-0.root"

treeOutputFilePath = "../trees_signal.root"

# histogramsOutputFilePath = "../histograms_signal.root"
histogramsOutputFilePath = "../histograms_HV.root"
# histogramsOutputFilePath = "../histograms_qcdCollider.root"
# histogramsOutputFilePath = "../histograms_dyCollider.root"

defaultHistParams = []

histParams = [
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
  
  ("InitialMuonsFromDarkPhoton", "pt"      ,    1000,  0,      1000,     ""),
  ("InitialMuonsFromDarkPhoton", "energy"  ,    100,  0,      10000,     ""),
  ("InitialMuonsFromDarkPhoton", "eta"     ,    100,  -10,    20,     ""),
  
  ("Event", "nZprimes"    ,    10,  0,      10,     ""),
  ("Event", "nDarkPhotons"    ,    10,  0,      10,     ""),
  ("Event", "nDarkHadrons",    10,  0,      10,     ""),
  ("Event", "nInitialMuons",    20,  0,      20,     ""),
  ("Event", "nGoodInitialMuons",    20,  0,      20,     ""),
  ("Event", "nGoodPtInitialMuons",    20,  0,      20,     ""),
  ("Event", "nMuonsHittingDetector",    20,  0,      20,     ""),
  ("Event", "nPtMuonsHittingDetector",    20,  0,      20,     ""),
  ("Event", "count",    1,  0,      1,     ""),
]

log_bins_10 = list(np.logspace(-7, 7, 150, base=10))
log_bins_10_extended = list(np.logspace(-50, 10, 610, base=10))

irregularHistParams = []

def addSingleHists(prefix):
  histParams.append((prefix, "pt"       ,    1000 ,  0    , 1000      ,     ""))
  histParams.append((prefix, "energy"   ,    200  ,  0    , 2000      ,     ""))
  histParams.append((prefix, "eta"      ,    100  ,  -10  , 20        ,     ""))
  histParams.append((prefix, "phi"      ,    100  ,  -4   , 4         ,     ""))
  histParams.append((prefix, "mass"     ,    100  ,  0    , 10        ,     ""))
  histParams.append((prefix, "pid"      ,    100  ,  0    , 10000000  ,     ""))
  histParams.append((prefix, "status"   ,    100  ,  0    , 100       ,     ""))
  histParams.append((prefix, "boost"    ,    100  ,  0    , 1         ,     ""))
  
  irregularHistParams.append((prefix, "d3d"         ,    log_bins_10,     ""))
  irregularHistParams.append((prefix, "properCtau"  ,    log_bins_10,     ""))

def addPairHists(prefix):
  histParams.append((prefix+"Pair", "deltaR"        ,    100  ,  0    ,      10 ,     ""))
  histParams.append((prefix+"Pair", "deltaEta"      ,    200  ,  -10  ,      10 ,     ""))
  histParams.append((prefix+"Pair", "deltaPhi"      ,    100  ,  0    ,      4  ,     ""))
  histParams.append((prefix+"Pair", "mass"          ,    1000 ,  0    ,      100,     ""))
  histParams.append((prefix+"Pair", "massCtauGt1cm" ,    1000 ,  0    ,      100,     ""))
  histParams.append((prefix+"Pair", "massCtauGt1m"  ,    1000 ,  0    ,      100,     ""))
  histParams.append((prefix+"Pair", "massCtauGt10m" ,    1000 ,  0    ,      100,     ""))
  
  irregularHistParams.append((prefix+"Pair", "muonsDistance"  ,    log_bins_10,     ""))
  irregularHistParams.append((prefix+"Pair", "dimuonVertexD3D"  ,    log_bins_10_extended,     ""))


for prefix in ["InitialMuons", "GoodInitialMuons", "GoodPtInitialMuons", "MuonsHittingDetector", "PtMuonsHittingDetector"]:
  addSingleHists(prefix)
  addPairHists(prefix)
  addPairHists(prefix+"SameVertex")  




# specify name of the branch containing event weights
weightsBranchName = "genWeight"

eventsTreeNames = ["Events",]
specialBranchSizes = {
  "Particle": "Event_numberP",
}

branchesToKeep = ["*"]
branchesToRemove = []
