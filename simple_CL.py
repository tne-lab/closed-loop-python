import zmqClasses
import stimmer.pyx
from queue import Queue


######################### THINGS TO CHANGE ###########################
CLTimer = 600             # Seconds
stimAddressX = 'Dev1/ao0' # stim
stimAddressY = 'Dev1/ao1'        # Sham
CLCHANNEL = 1             # CL event channel (out from last crossing detector)
CLMicroAmps = 100         # How many microamps
CLLag = 0                 # Wait? (almost zero for phase based CL, only used in plasticity)
CLTimeout = 1             # Timeout between stim
CLTimeoutVar = 0.2        # Timeout var
OE_Address = "localhost"  # localhost or ip address of other computer
record_dir = ""           # Where do you want data to be recorded
#############################################################


snd = zmqClasses.SNDEvent(OE_Address,5556, recordingDir = record_dir)
print('IF HANGS ADD NETWORK EVENTS TO OPEN EPHYS!!!')
snd.send( snd.STOP_REC)
snd.changeVars(prependText = 'CLOSED_LOOP')
snd.send( snd.START_REC)
stimX = daqAPI.AnalogOut( stimAddressX)
stimY = daqAPI.AnalogOut( stimAddressY)
stimQ = Queue()
stimBackQ = Queue()
stimmer.waitForEvent( stimX,  stimY,  stimQ,  stimBackQ,  CLCHANNEL,  CLMicroAmps,  CLLag, CLTimer,  CLTimeout,  CLTimeoutVar,  OE_Address))

# End tasks with daq so we can use them again
stimX.end()
stimY.end()
