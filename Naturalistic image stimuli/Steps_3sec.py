import QDS
import math

QDS.Initialize("Steps_RGBU")

# Define global stimulus parameters
p = {"nTrials"         : 50,     # Number of trials (Stimulus loop)

     "StimType"        : 1,       # Define Object shape (1 = Box, 2 = Circle)
     "dx_Stim"         : 7000,     # Stimulus width (>1500 for full screen)
     "dy_Stim"         : 7000,     # Stimulus height (>1500 for full screen)
     "Box_Angle"       : 0.0,     # Set the orientation of the box if StimType = 1

     "OffDur_s"        : 3.0,     # Off step duration in s
     "OnDur_s"         : 3.0,     # On step duration in s
     "PreAdapt_s"      : 2.0,     # Pre-Adaptation duration in s

     "x_pos"           : 0.0,     # Object x position (0 represents the center of the screen)
     "y_pos"           : 0.0,     # Object y position (0 represents the center of the screen)

     "Red_Iso"         : 255,     # Max Red intensity at "Equal Power"
     "Green_Iso"       : 255,     # Max Green intensity at "Equal Power"
     "Blue_Iso"        : 255,     # Max Blue intensity at "Equal Power"
     "UV_Iso"          : 255,     # Max UV intensity at "Equal Power"

     "Red_Nat"         : 25,      # Max Red intensity at "Nat stat Power"
     "Green_Nat"       : 25,      # Max Green intensity at "Nat stat  Power"
     "Blue_Nat"        : 25,      # Max Blue intensity at "Nat stat  Power"
     "UV_Nat"          : 25,      # Max UV intensity at "Nat stat  Power"

     "bkgCol_preadapt" : (25,25,25, 25,25,25),       # background color for Pre-Adaptation
     "bkgColor"        : (0,0,0, 0,0,0),       # background color

     "durFr_s"         : 1/60.0,  # Frame duration
     "nFrPerMarker"    : 3,       # Trigger duration in number of frames
     }


QDS.LogUserParameters(p)
durMarker_s     = p["durFr_s"]*p["nFrPerMarker"]     # Set Trigger duration in sec (3 * 1/60 = 0.05s by default)


# Define stimulus objects
QDS.DefObj_Box(1, p["dx_Stim"], p["dy_Stim"],p["Box_Angle"])
QDS.DefObj_Ellipse(2, p["dx_Stim"], p["dy_Stim"])


# Start of stimulus run
QDS.StartScript()

# Pre Adaptation
QDS.SetObjColor(1,[p["StimType"]], [(0,0,0,0,0,0)])                                         # Set Object Colour for Preadaptation
QDS.SetBkgColor(p["bkgCol_preadapt"])                                                       # Set Background Colour for Preadaptation
QDS.Scene_Render(p["PreAdapt_s"], 1, [p["StimType"]], [(p["x_pos"],p["y_pos"])], 0)         # Dispalay Preadaptation without trigger


for iL in range(p["nTrials"]):                                                              # For each Loop:

  ### Red ###########################################

  # On
  QDS.SetObjColor(1,[p["StimType"]], [(p["Red_Iso"],p["Green_Iso"],p["Blue_Iso"],p["UV_Iso"],p["UV_Iso"],p["UV_Iso"])])                                    # Set Object Colour
  QDS.SetBkgColor(p["bkgColor"])                                                                    # Set Background Colour
  QDS.Scene_Render(durMarker_s, 1, [p["StimType"]], [(p["x_pos"],p["y_pos"])], 1)                   # Display with trigger
  QDS.Scene_Render(p["OnDur_s"] - durMarker_s, 1, [p["StimType"]], [(p["x_pos"],p["y_pos"])], 0)    # Display without trigger

  # Off
  QDS.SetObjColor(1,[p["StimType"]], [(0,0,0,0,0,0)])                                               # Extinguish Object
  QDS.SetBkgColor(p["bkgColor"])                                                                    # Set Background Colour
  QDS.Scene_Render(p["OffDur_s"], 1, [p["StimType"]], [(p["x_pos"],p["y_pos"])], 0)                 # Off display without trigger


QDS.EndScript()

# -----------------------------------------------------------------------------
