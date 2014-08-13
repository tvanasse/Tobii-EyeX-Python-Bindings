from __future__ import print_function
from ctypes import *
from array import *
import time
import numpy as np
import matplotlib.pyplot as plt
from numpy import arange
import array
from tobiilib import struct
import sys, os

tobiiGazeCore64 = WinDLL(os.getcwd() + '\\tobiilib\\TobiiGazeCore64.dll');
tobiiGazeCore64.tobiigaze_get_connected_eye_tracker(struct.url, struct.URLsize, None)
eye_tracker = c_void_p(tobiiGazeCore64.tobiigaze_create(struct.url, None))
info = struct.tobii_device_info()
tobiiGazeCore64.tobiigaze_run_event_loop_on_internal_thread(eye_tracker, None, None)
tobiiGazeCore64.tobiigaze_connect(eye_tracker, byref(struct.errcode))
print("Connect status: %s" % struct.errcode)
tobiiGazeCore64.tobiigaze_get_device_info(eye_tracker, byref(info), byref(struct.errcode));
print("Device info status: %s" % struct.errcode)
print("Serial number: %r" % info.serial_number)
print("Model: %r" % info.model)
print("Generation: %r" % info.generation)
print("Firmware_version: %r" % info.firmware_version)


user_data = c_void_p()
tobiigaze_gaze_data_ref = byref(struct.tobiigaze_gaze_data())
tobiigaze_gaze_data_extensions_ref = byref(struct.tobiigaze_gaze_data_extensions())
eye_data_left = []
eye_data_right = []
#fo = open("output.txt", "w")
fo = sys.stdout

def on_gaze_data(tobiigaze_gaze_data_ref, tobiigaze_gaze_data_extensions_ref, user_data):
    gazedata = tobiigaze_gaze_data_ref.contents
    fo.write("\n%20.3f " % (gazedata.timestamp / 1e6)) #in seconds
    fo.write("%d " % gazedata.tracking_status)
       

    if (gazedata.tracking_status == struct.TOBIIGAZE_TRACKING_STATUS_BOTH_EYES_TRACKED or
        gazedata.tracking_status == struct.TOBIIGAZE_TRACKING_STATUS_ONLY_LEFT_EYE_TRACKED or
        gazedata.tracking_status == struct.TOBIIGAZE_TRACKING_STATUS_ONE_EYE_TRACKED_PROBABLY_LEFT):
        fo.write("[ %7.4f , %7.4f ] " % (gazedata.left.gaze_point_on_display_normalized.x, gazedata.left.gaze_point_on_display_normalized.y))
        lefteye = "[ %7.4f , %7.4f ] " % (gazedata.left.gaze_point_on_display_normalized.x, gazedata.left.gaze_point_on_display_normalized.y) 
        eye_data_left.append(lefteye)
    
    else:
        fo.write("[ %7s , %7s ] " % ("-", "-"))
        lefteye = "[ %7s , %7s ] " % ("-", "-")
        eye_data_left.append(lefteye)
        
    

    if (gazedata.tracking_status == struct.TOBIIGAZE_TRACKING_STATUS_BOTH_EYES_TRACKED or
        gazedata.tracking_status == struct.TOBIIGAZE_TRACKING_STATUS_ONLY_RIGHT_EYE_TRACKED or
        gazedata.tracking_status == struct.TOBIIGAZE_TRACKING_STATUS_ONE_EYE_TRACKED_PROBABLY_RIGHT):
        fo.write("[ %7.4f , %7.4f ] " % (gazedata.right.gaze_point_on_display_normalized.x, gazedata.right.gaze_point_on_display_normalized.y))
        righteye = "[ %7.4f , %7.4f ] " % (gazedata.right.gaze_point_on_display_normalized.x, gazedata.right.gaze_point_on_display_normalized.y)
        eye_data_right.append(righteye)
    
    else:
        fo.write("[ %7s , %7s ] " % ("-", "-"))
        righteye = "[ %7s , %7s ] " % ("-", "-")
        eye_data_right.append(righteye)
    return 0

callback_type = WINFUNCTYPE(c_int, POINTER(struct.tobiigaze_gaze_data), POINTER(struct.tobiigaze_gaze_data_extensions),
                            c_void_p)
tobiigaze_start_tracking = tobiiGazeCore64.tobiigaze_start_tracking
tobiigaze_start_tracking.restype = None
tobiigaze_start_tracking.argtypes = (c_void_p, callback_type, c_void_p, c_void_p)
on_gaze_data_func = callback_type(on_gaze_data)
tobiigaze_start_tracking(eye_tracker, on_gaze_data_func, byref(struct.errcode), None)

#Specify desired time of Gaze Data here
time.sleep(20)

tobiiGazeCore64.tobiigaze_stop_tracking(eye_tracker, byref(struct.errcode))
tobiiGazeCore64.tobiigaze_disconnect(eye_tracker)
print("ALL DONE")




