import zmqClasses
import stimmer
import daqAPI
import pandas as pd
import numpy as np
import os
from statistics import mean

######################### THINGS TO CHANGE ###########################
nERP = 4                 # EP per uA
stimAddressX = 'Dev1/ao0' # stim
startuA = 100             # uA to start at
enduA = 175               # uA to end at
stepSize = 25             # uA step size between start and end
OE_Address = "localhost"  # localhost or ip address of other computer
record_dir = ""           # Where do you want data to be recorded
#############################################################

snd = zmqClasses.SNDEvent(OE_Address,5556, recordingDir = record_dir)
print('IF HANGS ADD NETWORK EVENTS TO OPEN EPHYS!!!')
snd.send( snd.STOP_REC)
snd.changeVars(prependText = 'ERP_Titration')
snd.send( snd.START_REC)

stimX = daqAPI.AnalogOut( stimAddressX)
stimmer.ERPTitration(stimX, nERP, startuA, enduA, stepSize)
snd.send(snd.STOP_ACQ)

if(os.path.exists("E:\\test\\example.csv")):
    df = pd.read_csv("E:\\test\\example.csv")

if(~df.empty):
    splitdf = np.array_split(df,nERP) # Split into different amplitudes
    uAList = np.arange(startuA, enduA+1, stepSize) # How many steps
    ERPList = [0] * len(uAList)
    curMax = 0
    for i in range(len(uAList)):
        ERPList[i] = np.mean(splitdf[i], axis = 0)[0]

    halfAmp = max(ERPList) / 2 # What is our 50% amplitude
    index = np.argmin(np.abs(np.array(ERPList)-halfAmp))
    print(np.abs(np.array(ERPList)-halfAmp))
    print(ERPList)
    print(halfAmp)
    print(index)
    print('uA stimulation at 50% value : ' + str(uAList[index]))

