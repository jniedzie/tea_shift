## specify how many events to run on (and how often to print current event number)
nEvents = 100
printEveryNevents = 100

base_path = "/nfs/dust/cms/user/jniedzie/shift"

mZprime = 100
mDarkHadron = 20
mDarkQuark = 1

# skim = "pythia_test_events"
skim = f"pythia_mZprime-{mZprime}_mDH-{mDarkHadron}_mDQ-{mDarkQuark}_tau-1em7"

# specify input/output paths 
inputFilePath = f"{base_path}/merged_{skim}.root"
# inputFilePath = f"{base_path}/{skim}/mZprime-{mZprime}GeV_mDarkHadron-{mDarkHadron}GeV_mDarkQuark-{mDarkQuark}GeV_lifetime-1p00em07m_nEvents-100_part-0.root"

histogramsOutputFilePath = "../output_histograms.root"

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

# define custom 2D histograms (you will have to fill them in your HistogramsFiller)
histParams2D = (
#  name     bins_x  xmin  xmax bins_y ymin ymax     dir
  ("hit_xy", 100  , -20 , 20  , 100 , -20 , 20  ,   ""),
)

# specify name of the branch containing event weights
weightsBranchName = "genWeight"

eventsTreeNames = ["Events",]
specialBranchSizes = {
  "Particle": "Event_numberP",
}

detectorParams = {
  "x": 5,
  "y": 0,
  "z": 100,
  "radius": 10, 
}