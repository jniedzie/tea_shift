import ROOT

nEvents = -1

# on the ring:
# startingEvent = 0  # nice example, pencil like, large deviation in magnet
# startingEvent = 13  # also nice, one muon goes through the whole detector
# startingEvent = 43 # interesting, one makes it through
startingEvent = 54 # close to CMS, quite symetic, none makes it through


# off the ring:
# startingEvent = 0  # nice example ()

printEveryNevents = 100

magField = 2.0

showAxes = True

# doProjection = ""

# doProjection = "kCameraPerspXOZ"
# doProjection = "kCameraPerspYOZ"
# doProjection = "kCameraPerspXOY"

doProjection = "kCameraOrthoXOY"
# doProjection = "kCameraOrthoXOZ"
# doProjection = "kCameraOrthoZOY"
# doProjection = "kCameraOrthoZOX"

# doProjection = "kCameraOrthoXnOY"
# doProjection = "kCameraOrthoXnOZ"
# doProjection = "kCameraOrthoZnOY"
# doProjection = "kCameraOrthoZnOX"

inputFilePath = "../utils/example_signal.root"

eventsTreeNames = ["Events",]
specialBranchSizes = {"Particle": "Event_numberP",}

variant = "shift160m" # good for all signals
detectorParams = {
    "x": 160,
    "y": -1, # -1 means it will be placed on the LHC ring (based on the z coordinate)
    "z": 0,
    "radius": 7.5,
    "length": 22,
    "maxEta": 2.4,
}

backgroundColor = ROOT.kWhite
cmsColor = ROOT.kRed
shiftColor = ROOT.kBlue
