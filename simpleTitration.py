import zmqClasses
import stimmer
import daqAPI

######################### THINGS TO CHANGE ###########################
nERP = 20                 # EP per uA
stimAddressX = 'Dev1/ao0' # stim
startuA = 100             # uA to start at
enduA = 300               # uA to end at
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
    k = df.shape

if(~df.empty):
    ab = ((df.max(axis=1)-(df.max(axis=1)).max()*0.5).abs()).idxmin()
    selectedStimStep = int(ab/nERP)
    uAList = np.arange(startuA, enduA, stepSize)
    print('Stimulation at 50% value , ' + uAList[selectedStimStep])

