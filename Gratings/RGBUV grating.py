import QDS
import math
import numpy as np

QDS.Initialize("UV/Dark grating", "8-directional grating. Still, move, still.")

# Define global stimulus parameters
p = {"nTrials"         : 5,     # Number of trials (Stimulus loop)

     "StimType"        : 1,       # Define Object shape (1 = Box, 2 = Circle)
     "dx_Stim"         : 250.0,   # Bar width
     "dy_Stim"         : 4000.0,  # Bar heigh
     "Box_Angle"       : 0.0,     # Set the orientation of the box if StimType = 1

     "DirList"         : np.arange(0, 360, 45), # Direction list for the bar movement
     "vel_umSec"       : 800.0, # speed of moving bar in um/sec
     "tMoveDur_s"      : 3.0,    # duration of movement (defines distance the bar travels, not its speed)
     "IntervalDuration"  : 3.0,
     "PreAdapt_s"      : 5.0,    # Pre-Adaptation duration in s

     "bar_colour_preadapt": (150,150,150,150,150,150),
     "bar_colour"      : (255,255,255,255,255,255),
     "bkgCol_preadapt" : (100,100,100,100,100,100),       # background color for Pre-Adaptation
     "bkgColor"        : (0,0,0,0,0,0),       # background color

     "durFr_s"         : 1/60.0,  # Frame duration
     "nFrPerMarker"    : 3,       # Trigger duration in number of frames
    }

QDS.LogUserParameters(p)

# Do some calculations
durMarker_s    = p["durFr_s"]*p["nFrPerMarker"]         # Set Trigger duration in sec (3 * 1/60 = 0.05s by default)
freq_Hz        = round(1.0 /p["durFr_s"])
nX    = 8                                          # Number of Colums (Has to be an even number)
nY    = 1                                          # Number of Rows (Has to be an uneven number)
nFr   = 50                                          # Number of Frames
nB    = nX*nY                                       # Number of Boxes

moveDist_um    = p["vel_umSec"]*p["tMoveDur_s"]
umPerFr        = float(p["vel_umSec"]) /freq_Hz                                                 # For each Loop:
nFrToMove      = float(moveDist_um) /umPerFr

nTrial     = p['nTrials']
BoxIndList = []
BoxMagList = []
BoxPosList = []
BoxRotList = []

# Define stimulus objects
if (p["StimType"] == 1):
    for iB in range(1, nB+1):
        QDS.DefObj_Box(iB, p["dx_Stim"], p["dy_Stim"])  # Set the noise for boxes
if (p["StimType"] == 2):
    for iB in range(1, nB+1):
        QDS.DefObj_Ellipse(iB, p["dx_Stim"], p["dy_Stim"])  # Set the noise for circles

rot_deg = 0
rot_rad = (rot_deg)/360.0 *2 *math.pi

# Creating boxes index list and boxes position (coordinate) list
for iX in range(nX):
    iB = 1 +iX
    x  = math.cos(rot_rad) *(2*p["dx_Stim"]*iX - p["dx_Stim"]*nX/2)
    y  = math.sin(rot_rad) *(- 2*p["dx_Stim"]*iX + p["dx_Stim"]*nX/2)
    BoxIndList.append(iB)
    BoxMagList.append((1.0,1.0))
    BoxPosList.append((x,y))
    BoxRotList.append(rot_deg)

# Start of stimulus run
QDS.StartScript()

# Pre Adaptation
QDS.DefObj_EllipseEx("preadapt", 500, 500)
QDS.SetObjColorEx(["preadapt"], [p["bar_colour_preadapt"]])
QDS.SetBkgColor(p["bkgCol_preadapt"])                                                       # Set Background Colour for Preadaptation
QDS.Scene_RenderEx(p["PreAdapt_s"], ["preadapt"], [(1,1)], [(1,1)], [0], 0)      # Display a static grating at the start of the stimulus (no marker)

def GratingLooper():
    QDS.SetBkgColor(p["bkgColor"])                                                       # Set Background Colour for Preadaptation
    moveDist = 0
    for iB in range(nB):
        QDS.SetObjColorEx(BoxIndList, [p["bar_colour"]]*len(BoxIndList))
    for rot_deg in p["DirList"]:
      BoxRotList = []
      for iX in range(nX):
        BoxRotList.append(rot_deg)
      # Calculate rotation angle and starting position of bar
      rot_rad = (rot_deg)/360.0 *2 *math.pi
      # Move the bar stepwise across the screen (as smooth as permitted by the refresh frequency)
      for iStep in range(round(nFrToMove)):     #Move forward
        BoxPosList = []
        moveDist_temp  = moveDist + umPerFr
        moveDist = moveDist_temp
        if (moveDist>2*p["dx_Stim"]):
            moveDist = 0
        for iX in range(nX):
            x       = math.cos(rot_rad) *(2*p["dx_Stim"]*iX - p["dx_Stim"]*nX/2 - moveDist)
            y       = math.sin(rot_rad) *(-2*p["dx_Stim"]*iX + p["dx_Stim"]*nX/2 + moveDist)
            BoxPosList.append((x,y))
        if (iStep==0):
            QDS.Scene_RenderEx(durMarker_s, BoxIndList, BoxPosList, BoxMagList, BoxRotList, 1)
            QDS.Scene_RenderEx(p["IntervalDuration"], BoxIndList, BoxPosList, BoxMagList, BoxRotList, 0)
        QDS.Scene_RenderEx(p["durFr_s"], BoxIndList, BoxPosList, BoxMagList, BoxRotList, 0)
      for iStep in range(round(nFrToMove)):     #Move backward --> Did not need for this script, but keep for later...
#         BoxPosList = []
#         moveDist_temp  = moveDist - umPerFr
#         moveDist = moveDist_temp
#         if (moveDist<-2*p["dx_Stim"]):
#             moveDist = 0
#         for iX in range(nX):
#             x       = math.cos(rot_rad) *(2*p["dx_Stim"]*iX - p["dx_Stim"]*nX/2 - moveDist)
#             y       = math.sin(rot_rad) *(-2*p["dx_Stim"]*iX + p["dx_Stim"]*nX/2 + moveDist)
#             BoxPosList.append((x,y))
# #            QDS.Scene_Render(p["PreAdapt_s"], nB, BoxIndList, BoxPosList, BoxRotList)
        if (iStep==0):
            QDS.Scene_RenderEx(p["IntervalDuration"], BoxIndList, BoxPosList, BoxMagList, BoxRotList, 0)
        # QDS.Scene_RenderEx(p["durFr_s"], BoxIndList, BoxPosList, BoxMagList, BoxRotList, 0)


QDS.Scene_Clear(1.0, 0)
QDS.Loop(p["nTrials"], GratingLooper)

# Finalize stimulus
QDS.EndScript()

# --------------------------------------------------------------------------
