#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
import QDS
import math
import numpy as np

# --------------------------------------------------------------------------
def CircleMove():
  # A function that presents the moving bar in the given number of
  # directions (= moving bar sequence)
      
  for rot_deg in p["DirList"]:
     for sweep in p["StrtPosList"]:
            QDS.Scene_RenderEx(durMarker_s, [1], [(0,0)], [(0,0)], [0], 1)
            ## Calculate rotation angle and starting position of bar
            rot_rad = (rot_deg -90)/360.0 *2 *math.pi
            x       = math.cos(rot_rad) *(moveDist_um /2.0) + sweep
            y       = math.sin(rot_rad) *(-moveDist_um /2.0) + sweep
    
            ## Move the bar stepwise across the screen (as smooth as permitted
            ## by the refresh frequency)
            for iStep in range(round(nFrToMove)):
              QDS.Scene_RenderEx(p["durFr_s"], [1], [(x,y)], [(1.0,1.0)], [rot_deg])
              x    -= math.cos(rot_rad) *umPerFr
              y    += math.sin(rot_rad) *umPerFr
            # for jStep in range(round(nFrToMove)): #for moving backwards, but not needed if put in dirlist
            #   QDS.Scene_RenderEx(p["durFr_s"], [1], [(x,y)], [(1.0,1.0)], [rot_deg])
            #   x    += math.cos(rot_rad) *umPerFr
            #   y    -= math.sin(rot_rad) *umPerFr


# --------------------------------------------------------------------------
# Main script
# --------------------------------------------------------------------------
QDS.Initialize("", "")

# Define global stimulus parameters
radius = 100

p = {"nTrials"         : 1,
     "DirList"         : [45, 255, 135, 315],#[0, 180, 45, 225, 90, 270, 135, 315],
     "StrtPosList"     : np.arange(-100, 100, radius),

     "vel_umSec"       : 500.0, # speed of moving bar in um/sec
     "tMoveDur_s"      : 5.0,    # duration of movement (defines distance
                                 # the bar travels, not its speed)
     "barDx_um"        : radius,  # bar dimensions in um
     "barDy_um"        : radius,
     "bkgColor"        : (0,0,0,0,0,0),       # background color
     "barColor"        : (255, 255,255,255, 255, 255), # bar color
     "durFr_s"         : 1/60.0, # Frame duration
     "nFrPerMarker"    : 3
    }
QDS.LogUserParameters(p)

# Do some calculations
#
durMarker_s    = p["durFr_s"]*p["nFrPerMarker"]
freq_Hz        = round(1.0 /p["durFr_s"])
umPerFr        = float(p["vel_umSec"]) /freq_Hz
moveDist_um    = p["vel_umSec"] *p["tMoveDur_s"]
nFrToMove      = float(moveDist_um) /umPerFr

print(nFrToMove, int(nFrToMove), int(nFrToMove)*p["durFr_s"], durMarker_s)
# Define stimulus objects
#
QDS.DefObj_Ellipse(1, p["barDx_um"], p["barDy_um"])

# Start of stimulus run
#
QDS.StartScript()

QDS.SetObjColor(1, [1], [p["barColor"]])
QDS.SetBkgColor(p["bkgColor"])
QDS.Scene_Clear(3.0, 0)

# Loop the moving bar sequence nTrial times
#
QDS.Loop(p["nTrials"], CircleMove)

QDS.Scene_Clear(1.0, 0)

# Finalize stimulus
#
QDS.EndScript()

# --------------------------------------------------------------------------
