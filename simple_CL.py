import pyximport; pyximport.install()
import zmqClasses
import stimmer
import daqAPI
from tkinter import *
import time
from queue import Queue


######################### THINGS TO CHANGE ###########################
CLTimer = 1800           # Seconds 3600 (How long to run closed loop)
stimAddressX = 'Dev1/ao0' # stim
stimAddressY = 'Dev1/ao1' # Sham
CLCHANNEL = 1             # CL event channel (out from last crossing detector)
CLMicroAmps = 500         # How many microamps (100ua/V) - 90micro sec biphasic pulse
CLLag = 0                 # Wait? (almost zero for phase based CL, only used in plasticity)
CLTimeout = 1             # Timeout between stim
CLTimeoutVar = 0.2        # Timeout var
OE_Address = "localhost"  # localhost or ip address of other computer
record_dir = "D:\\EPHYSDATA\\dev2110\\day3"           # Where do you want data to be recorded
watchChannel = '8-1' # what channel did you watch for phase '1-2' would mean channel 1 was watched and was bipoled with channel 2
freqRange = [4, 12] # what freq range (just for logging purposes, doesn't change anything in OE itself)

## ERPS
nERP = 1 # How many ERPS
ERPTOmin = 3 # ERP timeout min and max
ERPTOmax = 5
nERPLoc = 1 # How many locations to do ERP in

## Raw 
rawTime = 5 # In minutes
#############################################################

recordingList = []

snd = zmqClasses.SNDEvent(OE_Address,5556, recordingDir = record_dir)
print('IF HANGS ADD NETWORK EVENTS TO OPEN EPHYS!!!')
snd.send(snd.STOP_REC)
stimX = daqAPI.AnalogOut( stimAddressX)
stimY = daqAPI.AnalogOut( stimAddressY)
stimQ = Queue()
stimBackQ = Queue()

# Raw pre
print('starting raw pre')
snd.send(snd.STOP_REC)
snd.changeVars(prependText = 'RAW_PRE')
snd.send(snd.START_REC)
time.sleep(rawTime*60) # 
snd.send(snd.STOP_REC)
recordingList.append('RAW_PRE')

# ERP Pre
#print('Starting ERP pre')
#stimmer.ERP(stimX, stimY, stimQ, stimBackQ, nERP, ERPTOmin, ERPTOmax, nERPLoc, snd, 'PRE', 5) # send out 5 volts for stimjim

#snd.send(snd.STOP_REC)
print('starting closed loop')
snd.changeVars(prependText = 'CLOSED_LOOP')
snd.send(snd.START_REC)
stimmer.waitForEvent( stimX,  stimY,  stimQ,  stimBackQ,  CLCHANNEL,  CLMicroAmps,  CLLag, CLTimer,  CLTimeout,  CLTimeoutVar,  OE_Address)
snd.send(snd.STOP_REC)
recordingList.append('CLOSED_LOOP')

# ERP Post
#print('starting erp post')
#stimmer.ERP(stimX, stimY, stimQ, stimBackQ, nERP, ERPTOmin, ERPTOmax, nERPLoc, snd, 'POST')
#snd.send(snd.STOP_REC)

window = Tk()
winText = "Unplug stim wires for cleaner raw data! \n Close window to continue"
lbl = Label(window, text=winText, font=("Arial Bold", 100))
lbl.grid(column=0, row=0)
window.mainloop()

# Raw post
print('starting raw post')
snd.send(snd.STOP_REC)
snd.changeVars(prependText = 'RAW_POST')
snd.send(snd.START_REC)
recordingList.append('RAW_POST')

time.sleep(rawTime*60)
snd.send(snd.STOP_ACQ)

# End tasks with daq so we can use them again
stimX.end()
stimY.end()



## Create log file
from scipy.io import savemat
matdic = {}
# save data folders
matdic['paths'] = recordingList
# save data vars from above
matdic['CLTimer'] = CLTimer             # minutes 
matdic['stimAddressX'] =stimAddressX # stim
matdic['stimAddressY'] =stimAddressY         # Sham
matdic['CLCHANNEL'] =CLCHANNEL            # CL event channel (out from last crossing detector)
matdic['CLMicroAmps'] =CLMicroAmps         # How many microamps
matdic['CLLag'] =CLLag              # seconds to sleep between event recieved and sending out stim. Also can use a list ie [0, 5] to wait randomly between 0 and 5 seconds after event
matdic['CLTimeout'] =CLTimeout              # Timeout between stim
matdic['CLTimeoutVar'] =CLTimeoutVar         # Timeout var
matdic['OE_Address'] =OE_Address   # localhost or ip address of other computer
matdic['record_dir'] =record_dir         # Where do you want data to be recorded
matdic['watchChannel'] =watchChannel  # what channel did you watch for phase '1-2' would mean channel 1 was watched and was bipoled with channel 2
matdic['freqRange'] =freqRange # what freq range

## ERPS
matdic['nERP'] =nERP  # How many ERPS
matdic['ERPTOmin'] =ERPTOmin  # ERP timeout min and max
matdic['ERPTOmax'] =ERPTOmax 
matdic['nERPLoc'] =nERPLoc # How many locations to do ERP in

## Raw 
matdic['rawTime'] =rawTime # In minutes



savemat(record_dir + '\\log_file.mat', matdic)
