import sys
import os

# Add the directory containing shift_paths.py to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from shift_paths import detectorParams, base_path, variant

nEvents = -1
printEveryNevents = 100
inputFilePath = "../utils/example_signal.root"

eventsTreeNames = ["Events",]
specialBranchSizes = {
  "Particle": "Event_numberP",
}
