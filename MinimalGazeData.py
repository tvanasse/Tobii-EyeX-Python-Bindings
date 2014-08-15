import time
import os
from ctypes import *
from tobiilib import struct

print('here')
print(os.getcwd())

tobiiGazeCore64 = WinDLL(os.getcwd() + '\\tobiilib\\TobiiGazeCore64.dll');
struct.start_tracking()

#Specify desired time of Gaze Data here
time.sleep(3)

struct.stop_tracking()


print("ALL DONE")




