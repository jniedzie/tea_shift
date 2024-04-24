from shift_paths import skim

## specify how many events to run on (and how often to print current event number)
nEvents = 1000
printEveryNevents = 100

base_path = "/nfs/dust/cms/user/jniedzie/shift"

# process = "pythia_qcd"
# process = "pythia_dy"    
# process = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1e3"
process = "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7"

# specify input/output paths 
inputFilePath = f"{base_path}/{process}/merged_{skim}.root"
histogramsOutputFilePath = f"../histograms_{skim}_{process}.root"

# inputFilePath = "./skimmed_test.root"
# histogramsOutputFilePath = "../histograms_test.root"

# define default histograms (can be filled automatically with HistogramsFiller, based on collection and variable names)
defaultHistParams = (
#  collection      variable          bins    xmin     xmax     dir
  ("Particle"        , "px"            , 400,    0,       200,     ""  ),
)

# define custom histograms (you will have to fill them in your HistogramsFiller)
histParams = (
#    name                 bins  xmin    xmax    dir
  ("Zprime", "pt"  ,      100,  0,      1000,     ""),
  ("Zprime", "eta" ,      100,  -10,    20,     ""),
  ("Zprime", "phi" ,      100,  -4,     4,     ""),
  ("Zprime", "mass",      100,  0,      500,     ""),
  ("Zprime", "pid"  ,     100,  0,      10000000,     ""),
  ("Zprime", "status",    100,  0,      100,     ""),
  
  ("DarkHadron", "pt"  ,      100,  0,      1000,     ""),
  ("DarkHadron", "eta" ,      100,  -10,    20,     ""),
  ("DarkHadron", "phi" ,      100,  -4,     4,     ""),
  ("DarkHadron", "mass",      100,  0,      10,     ""),
  ("DarkHadron", "pid"  ,     100,  0,      10000000,     ""),
  ("DarkHadron", "status",    100,  0,      100,     ""),
  
  ("MuonFromDarkHadron", "pt"      ,    100,  0,      1000,     ""),
  ("MuonFromDarkHadron", "energy"  ,    100,  0,      10000,     ""),
  ("MuonFromDarkHadron", "eta"     ,    100,  -10,    20,     ""),
  ("MuonFromDarkHadron", "phi"     ,    100,  -4,     4,     ""),
  ("MuonFromDarkHadron", "mass"    ,    100,  0,      10,     ""),
  ("MuonFromDarkHadron", "pid"     ,    100,  0,      10000000,     ""),
  ("MuonFromDarkHadron", "status"  ,    100,  0,      100,     ""),
  ("MuonFromDarkHadron", "x"  ,    100,  -10000000,      10000000,     ""),
  ("MuonFromDarkHadron", "y"  ,    100,  -10000000,      10000000,     ""),
  ("MuonFromDarkHadron", "z"  ,    100,  -1000000000,      1000000000,     ""),
   
  ("Event", "nZprimes"    ,    10,  0,      10,     ""),
  ("Event", "nDarkHadrons",    100,  0,      100,     ""),
  ("Event", "nMuonsFromDarkHadrons",    100,  0,      100,     ""),
)

# specify name of the branch containing event weights
weightsBranchName = "genWeight"

eventsTreeNames = ["Events",]
specialBranchSizes = {
  "Particle": "Event_numberP",
}
