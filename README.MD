# Simple code to implement TNEL closed loop protocol in Python

Note: Need to grab updates from Erics computer!

Make sure network events and event broadcaster are in the Open Ephys signal chain.

## To Use closed looop
Update variables in simple_CL.py and run to start closed loop.


## To use titration
Update variables in simpleTitration.oy and run to start titration to determine the "correct" amplitude of stimulation. (50% of max response)

simpleTitration.py needs real-time-ERP in Open Ephys. If path ```if(os.path.exists("E:\\test\\example.csv")):``` doesn't exist on your system (ie don't have an E: drive) talk to <markschatza@gmail.com> to update the real-timeERP plugin. 

Plugin can be found here.
https://github.com/tne-lab/real-time-ERP