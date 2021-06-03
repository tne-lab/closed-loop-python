import pyximport; pyximport.install()
import zmqClasses
import stimmer
import daqAPI
from tkinter import *
import time
from queue import Queue


######################### THINGS TO CHANGE ###########################
nERP = 40                 # EP per uA
stimAddressX = 'Dev1/ao0' # stim
startuA = 100
#startuA = 250             # uA to start at
enduA = 300               # uA to end at
stepSize = 25             # uA step size between start and end
OE_Address = "localhost"  # localhost or ip address of other computer
record_dir = "D:\\test"           # Where do you want data to be recorded
#############################################################
snd = zmqClasses.SNDEvent(OE_Address,5556, recordingDir = record_dir)
print('IF HANGS ADD NETWORK EVENTS TO OPEN EPHYS!!!')
snd.send( snd.STOP_REC)
snd.changeVars(prependText = 'ERP_Titration')
snd.send( snd.START_REC)

stimX = daqAPI.AnalogOut( stimAddressX)
stimmer.ERPTitration(stimX, nERP, startuA, enduA, stepSize)

###################################################################


# snd = zmqClasses.SNDEvent(OE_Address,5556, recordingDir = record_dir)
# print('IF HANGS ADD NETWORK EVENTS TO OPEN EPHYS!!!')
# snd.send(snd.STOP_REC)
# stimX = daqAPI.AnalogOut( stimAddressX)
# stimY = daqAPI.AnalogOut( stimAddressY)
# stimQ = Queue()
# stimBackQ = Queue()

# # Raw pre
# print('starting raw pre')
# snd.send(snd.STOP_REC)
# snd.changeVars(prependText = 'RAW_PRE')
# snd.send(snd.START_REC)
# time.sleep(rawTime*60) # 15 mins
# snd.send(snd.STOP_REC)

# # ERP Pre
# print('Starting ERP pre')
# stimmer.ERP(stimX, stimY, stimQ, stimBackQ, nERP, ERPTOmin, ERPTOmax, nERPLoc, snd, 'PRE')

# snd.send(snd.STOP_REC)
# print('starting closed loop')
# snd.changeVars(prependText = 'CLOSED_LOOP')
# snd.send(snd.START_REC)
# stimmer.waitForEvent( stimX,  stimY,  stimQ,  stimBackQ,  CLCHANNEL,  CLMicroAmps,  CLLag, CLTimer,  CLTimeout,  CLTimeoutVar,  OE_Address)

# # ERP Post
# print('starting erp post')
# stimmer.ERP(stimX, stimY, stimQ, stimBackQ, nERP, ERPTOmin, ERPTOmax, nERPLoc, snd, 'POST')
# snd.send(snd.STOP_REC)

# window = Tk()
# winText = "Unplug stim wires! \n Close window to continue"
# lbl = Label(window, text=winText, font=("Arial Bold", 100))
# lbl.grid(column=0, row=0)
# window.mainloop()

# # Raw post
# print('starting raw post')
# snd.send(snd.STOP_REC)
# snd.changeVars(prependText = 'RAW_POST')
# snd.send(snd.START_REC)

# time.sleep(rawTime*60)
# snd.send(snd.STOP_ACQ)

# End tasks with daq so we can use them again
stimX.end()
#stimY.end()
