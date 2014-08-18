#!/usr/bin/env python

#############################################################################
##
## Authors: Tom Vanasse and Nate Vack
##
## This program returns gaze data from both eyes for a specified period of 
## time.  The gaze Screen coordinates returned are the x and y coordinates, each 
## ranging from 0 to 1.  The point (0, 0) denotes the upper left corner and 
## (1, 1) the lower right corner of the Active Display Area.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

import time
import os
from ctypes import *

from tobii_lib import struct

print(os.getcwd())

tobiiGazeCore64 = WinDLL(os.getcwd() + '\\tobii_lib\\TobiiGazeCore64.dll');
struct.start_tracking()

#Specify desired time of Gaze Data here
time.sleep(3)

struct.stop_tracking()

print("ALL DONE")




