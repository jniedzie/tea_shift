## specify how many events to run on (and how often to print current event number)
nEvents = 1000
printEveryNevents = 100

# specify input/output paths 
# inputFilePath = "/nfs/dust/cms/user/jniedzie/shift/merged_pythia_test_events.root"
inputFilePath = "/nfs/dust/cms/user/jniedzie/shift/pythia_test_events/mZprime-100GeV_mDarkHadron-2GeV_mDarkQuark-1GeV_lifetime-1p00em07m_nEvents-100_part-0.root"
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
  
  ("Event", "nZprimes"    ,    10,  0,      10,     ""),
  ("Event", "nDarkHadrons",    100,  0,      100,     ""),
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