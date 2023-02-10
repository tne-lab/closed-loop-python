# Last updated 22Jul2022 by JHW
# NOTE: Video/Ephys are approximately concurrent. Start and stop times are prone to slight mismatch.

### Stripped this down significantly for needs of this project (JHW Jan 5, 2023)

print('Importing Required Libraries')
import json
import threading
import time
import os

#import tkinter
from tkinter import *
from queue import Queue

from scipy.io import savemat
import pyximport; pyximport.install()

import daqAPI
# import dev_cam as cam
import stimmer_blackrock as stimmer # Changed to run with Blackrock
import zmqClasses


print('Libraries Successfully Imported!')
######################### THINGS TO CHANGE ###########################
CLTimer = 1800
CLTimerLocked = 10 # Seconds 1800 (How long to run closed loop)
#CLTimerPre = 600 # seconds for section to let TORTE lock to 180 degrees, added 12/17/2021
CLTimerPre = 6 # seconds for section to let TORTE lock to 180 degrees, added 12/17/2021
stimAddressX = 'Dev1/ao0' # stim
stimAddressY = 'Dev1/ao1' # Sham
CLCHANNEL = 1             # CL event channel (out from last crossing detector)
# Change back to 500 for stimjim
CLMicroAmps = 500         # How many microamps (100ua/V) - 90micro sec biphasic pulse
CLLag = 0                 # Wait? (almost zero for phase based CL, only used in plasticity)
CLTimeout = .250             # Timeout between stim
CLTimeoutVar = 0.02        # Timeout var
OE_Address = "localhost"  # localhost or ip address of other computer
patient = '002'
day = '001'
drive = "D:" # drive where the data is written - This should be the same on all device project computers.
# If you are getting video save issues or path errors for saving .mat file, try changing to raw string with manual '\\' added: eg: r"D:\\"
drive_folder = 'EPHYSDATA'
record_dir = os.path.join(drive, drive_folder, patient, day) # os.path is the clean way of formatting paths between unix/windows platforms
watchChannel = '1-2' # what channel did you watch for phase '1-2' would mean channel 1 was watched and was bipoled with channel 2
freqRange = [4, 8] # what freq range (just for logging purposes, doesn't change anything in OE itself)

### Recording Conditions ###
light_type = 'Ambient' # Were lights on in the chamber? If not LED or puck light, maybe 'OFF'?
light_color = 'N/A'
door_open = False # Was the door of the chamber open or closed? Boolean value is my first thought for this
erps = False # Was erp section included in the recording protocol?
rec_by = 'JHW' # Who did the recording?
rec_comp = "Rig 8 (Diehl Cart)"
rec_notes = 'ATLAS DEMO: Mayo Hall a470. Using ATLAS'# Blank by default

### ERP Parameters ###
nERP = 5 # How many ERPS [50]
ERPTOmin = 3 # ERP timeout min and max
ERPTOmax = 5
nERPLoc = 2 # How many locations to do ERP in

### Raw Parameters ###
rawTime = 1 # In minutes [5]

### Additional Parameters ###
recordingList = []
snd = zmqClasses.SNDEvent(OE_Address,5556, recordingDir = record_dir)
print('IF HANGS ADD NETWORK EVENTS TO OPEN EPHYS!!!')
snd.send(snd.STOP_REC)
stimX = daqAPI.AnalogOut( stimAddressX)
stimY = daqAPI.AnalogOut( stimAddressY)
stimQ = Queue()
stimBackQ = Queue()

##### ADDED SECTION JAN 5, 2023 (JHW) #####

### ATLAS REC ###
print('ATLAS_REC')
snd.send(snd.STOP_REC)
snd.changeVars(prependText = 'ATLAS_REC')
snd.send(snd.START_REC)
print('SENT REC *START* SIGNAL')
stimmer.waitForEvent( stimX,  stimY,  stimQ,  stimBackQ,  CLCHANNEL,  CLMicroAmps,  CLLag, CLTimer,  CLTimeout,  CLTimeoutVar,  OE_Address)
print('SENT REC *STOP* SIGNAL')
snd.send(snd.STOP_REC)
recordingList.append('ATLAS_REC')

### Turned off remaining conditions at this time - may become relevant again in summer 2023 ###

# End tasks with daq so we can use them again
stimX.end()
stimY.end()