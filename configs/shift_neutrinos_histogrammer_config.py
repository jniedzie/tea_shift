from shift_neutrinos_paths import detectorParams, base_path, variant
import numpy as np

import sys
import os

# Add the directory containing shift_paths.py to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# specify how many events to run on (and how often to print current event number)
nEvents = -1

inputFilePath = f"{base_path}/pythia_qcd/initial/qcd_part-0.root"
# inputFilePath = f"{base_path}/pythia_dy/initial/dy_part-0.root"

treeOutputFilePath = "../trees_neutrinos.root"
histogramsOutputFilePath = "../histograms_neutrinos.root"

defaultHistParams = []

histParams = [
  #    name                 bins  xmin    xmax    dir
  ("Event", "nInitialNeutrinos", 100, 0, 100, ""),
  ("Event", "nNeutrinosHittingDetector", 100, 0, 100, ""),
  ("Event", "count", 1, 0, 1, ""),
]

log_bins_10 = list(np.logspace(-7, 7, 150, base=10))
log_bins_10_extended = list(np.logspace(-50, 10, 610, base=10))

irregularHistParams = []

for prefix in ["InitialNeutrinos", "NeutrinosHittingDetector"]:
  histParams.append((prefix, "pt", 1000, 0, 1000, ""))
  histParams.append((prefix, "energy", 200, 0, 2000, ""))
  histParams.append((prefix, "eta", 100, -10, 20, ""))
  histParams.append((prefix, "phi", 100, -4, 4, ""))
  histParams.append((prefix, "mass", 100, 0, 10, ""))
  histParams.append((prefix, "pid", 100, 0, 10000000, ""))
  histParams.append((prefix, "status", 100, 0, 100, ""))
  histParams.append((prefix, "boost", 100, 0, 1, ""))
  irregularHistParams.append((prefix, "d3d", log_bins_10, ""))
  irregularHistParams.append((prefix, "properCtau", log_bins_10, ""))

eventsTreeNames = ["Events"]
specialBranchSizes = {"Particle": "Event_numberP"}

branchesToKeep = [
  "Event_numberP",
  "Particle_barcode",
  "Particle_x",
  "Particle_y",
  "Particle_z",
  "Particle_px",
  "Particle_py",
  "Particle_pz",
  "Particle_energy",
  "Particle_pid",
]
