# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 15:36:24 2021

@author: skrem
"""

import QDS
import skimage.io
import os
import pathlib

# import glob Not in use at the 'mo

p = {
# General stim
'nTrials'       :   3,                       # number of stimulus presentations

# Movie
'mScal'         :   (10, 10),              # movie scaling (x, y)
'mOrient'       :   0,#[0, 45, 90, 135]      # movie orientations
'mAlpha'        :   255,                     # transparency of movie (255 is opaque)
# 'num_frames':30 # get this through QDS.GetMovieParameters and update p (params dict)

# Timing
'display_time_s':   2,
'blank_time_s'  :   1,
'marker_dur_s'  :   0.1,

# Colours
# 'blanking_col'  :   (127, 127, 127, 127, 127, 127),      # color of blanking stim
'background_col':   (0, 0, 0, 0, 0, 0), # background colour (which is now also blanking stim)

# Pathing
'img_file_name' :   "test_img_mono.png", # name of file to be displayed from QDSpy stimulus folder
# 'QDSpy_stimpath':   "C://Users\SimenLab\QDSpy\Stimuli", # path for QDSpy stimulus folder
'QDSpy_stimpath':   pathlib.Path(__file__), # path for QDSpy stimulus folder
# 'stimfile_path' :   pathlib.Path(__file__).parent.resolve(), # not in use
}

# Preperation
org_dir = os.getcwd() # make note of current working directory
QDS.Initialize() # initialise QDS
QDS.SetBkgColor(p['background_col']) # set background colour to be used

# Get stimulus
QDS.DefObj_Movie(1, "test_img_mono.png") #gets this from stimulus folder defined in QDS.ini and specified in dict p
p.update(QDS.GetMovieParameters(1)) #gets p['nFr'] from corresponding .txt file and updates dictionary p
# "dxFr", "dyFr", and "nFr"

# Make UV stimulus component
os.chdir(p['QDSpy_stimpath'].parent) # change directory to QDSpy stimulus folder (same one as specified in .ini)
mono_img = skimage.io.imread(p["img_file_name"]) # open mono image series
def make_txt_file_for_mono(fname, copy = True): # create accompanying .txt file for QDSpy
    lines = ['[QDSMovie2Description]', 'QDSVersionID=xQDS', 'FrWidth={}'.format(p["dxFr"]), 'FrHeight={}'.format(p["dyFr"]), 'FrCount={}'.format(
        p["nFr"]), 'isFirstFrBottomLeft=True', 'Comment=na']  # automatically get previously established frame parameters
    # use 'with' to ensure .txt file is opened then closed
    with open('{}.txt'.format(fname), 'w') as f:
        for line in lines:
            f.write(line)
            f.write('\n')
    return
"""
TODO
"""
# def check_for_mono_txt(target_file):
#     for file in glob.glob(".txt"):
#         if file == target_file:
#             file_exists = True
#             return file_exists
#         else:
#             file_exists = False
#             return file_exists

make_txt_file_for_mono("test_img_mono") # call above function
os.chdir(org_dir) # change back to oringinal working directory just to be safe
# QDS.DefObj_Movie(2, "test_img_mono.png") # define the UV movie object with newly created files

# Define blanking stimulus (currently just using background instead)
# QDS.DefObj_Box(3, 2500, 2500)
# QDS.SetObjColorEx([3], [p["blanking_col"]])

# Convert from seconds to frames
FrRefr_Hz = QDS.GetDefaultRefreshRate()
display_time = FrRefr_Hz * p['display_time_s']
blank_time = FrRefr_Hz * p['blank_time_s']

"""
TIP
You need to put QDS.Scene_Clear either before or after QDS.Start_Movie.
Otherwise, Start_Movie does nothing.

After seems better, as the first image is not preceeded by blanking.

See loop function below:
"""
# Loop for displaying stimulus
def loop():
    QDS.Scene_Clear(0.00, 0) # Clear scene and prepare stims
    for i in range(p['nFr']): # Loop through i amount of frames in file (as specified by .txt)
        # Display img i:
        QDS.Scene_Clear(p['marker_dur_s'] , 1) # display momentary marker
        QDS.Start_Movie(1, (0,0), [i, i, display_time, 1], p['mScal'], p['mAlpha'], p['mOrient'], _screen=0) #Display RGB image
        # QDS.Start_Movie(2, (0,0), [i, i, display_time, 1], p['mScal'], p['mAlpha'], p['mOrient'], _screen=1) #Display UV image simultaneously
        QDS.Scene_Clear(p['display_time_s'] , 0) #Need this for Start_Movie to work
        # Give blank stimulus between frames
        if p['blank_time_s'] > 0:
            ## Display "nothing" (clear scene for x amount of seconds)
            QDS.Scene_Clear(p['blank_time_s'], 0)
        if p['blank_time_s'] == 0:
            QDS.Scene_Clear(0.00000000000000000000000001, 0)
            # QDS.Scene_RenderEx(p["blank_time_s"], [3], [(0, 0)], [(1, 1)], [0]) # (alternative using box object)
    return


QDS.StartScript()
QDS.Loop(p['nTrials'], loop)
QDS.EndScript()

# This was a good idea, but the monochromatic files have to persist to function
# when playing the stimulus...
# os.remove(p['QDSpy_stimpath'] + '/' + 'test_img_mono.png')
# os.remove(p['QDSpy_stimpath'] + '/' + 'test_img_mono.txt')
