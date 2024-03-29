# Simple code to implement TNEL closed loop protocol in Python

Start Open Ephys and load in config file. Examples included in ```config``` folder.

If making your own signal chain make sure network events and event broadcaster are in the Open Ephys signal chain!

## To Use closed looop
Update variables in simple_CL.py and run to start closed loop.


## To use titration
Update variables in simpleTitration.py and run to start titration to determine the "correct" amplitude of stimulation. (50% of max response)

simpleTitration.py needs real-time-ERP in Open Ephys. If path ```if(os.path.exists("E:\\test\\example.csv")):``` doesn't exist on your system (ie don't have an E: drive) talk to <markschatza@gmail.com> to update the real-timeERP plugin. 

Plugin can be found here.
https://github.com/tne-lab/real-time-ERP


## Code info

simpleCL.py - Holds a script that runs a typical TNEL closed loop stim experiment. Consisting of raw rec -> Event related potential (ERP) stims -> closed loop stim -> ERP -> raw rec. Variables at the top can be used to define experiment and stim parameters. 

zmqClasses.py - Holds code to communicate bi-directionaly with Open Ephys. Telling it to start and stop recordings for each section of the experiment (with a network events plugin in OE). As well as recieving events (from an event broadcaster in OE).

daqAPI.py - Used to control the behvaior chambers for our rodent models and connects our stim trigger outputs. 

stimmer.pyx - Cython code (pyx) that runs faster than normal python. Contains our stimulation protocols and logic. Closed loop (waitForEvent()), ERP (ERP), and more stimulation paradigms we've used. 
