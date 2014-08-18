#!/usr/bin/env python

#############################################################################
##
## Authors: Tom Vanasse and Nate Vack
##
## This file provides the c_type python structures necessary to 
## run simple funtions with the Tobii Eyex Engine, as well as some basic
## functions of its own  This file works with the 'TobiiGazeCore64.dll' found 
## here: http://developer.tobii.com/eyex-sdk/.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

from __future__ import print_function
import array 
import os
import matplotlib.pyplot as plt 
from ctypes import *

TOBIIGAZE_TRACKING_STATUS_NO_EYES_TRACKED = 0
TOBIIGAZE_TRACKING_STATUS_BOTH_EYES_TRACKED = 1
TOBIIGAZE_TRACKING_STATUS_ONLY_LEFT_EYE_TRACKED = 2
TOBIIGAZE_TRACKING_STATUS_ONE_EYE_TRACKED_PROBABLY_LEFT = 3
TOBIIGAZE_TRACKING_STATUS_ONE_EYE_TRACKED_UNKNOWN_WHICH = 4
TOBIIGAZE_TRACKING_STATUS_ONE_EYE_TRACKED_PROBABLY_RIGHT = 5
TOBIIGAZE_TRACKING_STATUS_ONLY_RIGHT_EYE_TRACKED = 6
TOBIIGAZE_MAX_GAZE_DATA_EXTENSIONS = 32
URL_SIZE = c_uint32(256);

url = create_string_buffer(256);
errcode = c_uint32()


class TobiiDeviceInfo(Structure):
    
    _fields_ =[("serial_number", c_char * 128), ("model", c_char * 64),
               ("generation", c_char * 64), ("firmware_version", c_char * 128)
               ]
               
class TobiigazePoint3d(Structure):
    
    _fields_ = [("x", c_double), ("y", c_double), ("z", c_double)]

class TobiigazePoint2d(Structure):
    
    _fields_ = [("x", c_double), ("y", c_double)]

class TobiiGazeDataEye(Structure):
    
    _fields_ = [("eye_position_from_eye_tracker_mm", TobiigazePoint3d),
                ("eye_position_in_track_box_normalized", TobiigazePoint3d),
                ("gaze_point_from_eye_tracker_mm", TobiigazePoint3d),
                ("gaze_point_on_display_normalized", TobiigazePoint3d)
                ]
    
class TobiiGazeData(Structure):
    
    _fields_ = [("timestamp", c_uint64), ("tracking_status", c_uint),
                ("left", TobiiGazeDataEye), 
                ("right", TobiiGazeDataEye)
                ]

class TobiiGazeDataExtension(Structure):
    
    _fields_ = [("column_id", c_uint32), ("data", c_uint8 * 256), 
                ("actual_size", c_uint32)
                ]


class TobiiGazeDataExtensions(Structure):
    
    _fields_ = [("extensions", 
                 TobiiGazeDataExtension * TOBIIGAZE_MAX_GAZE_DATA_EXTENSIONS), 
                 ("actual_size", c_uint32)
                 ]

def on_gaze_data(tobiigaze_gaze_data_ref, tobiigaze_gaze_data_extensions_ref, 
                 user_data
                 ):
                     
    gazedata = tobiigaze_gaze_data_ref.contents
    print("%20.3f " % (gazedata.timestamp / 1e6), end = "") #in seconds
    print("%d " % gazedata.tracking_status, end = "")
       
    if (gazedata.tracking_status == TOBIIGAZE_TRACKING_STATUS_BOTH_EYES_TRACKED or
        gazedata.tracking_status == TOBIIGAZE_TRACKING_STATUS_ONLY_LEFT_EYE_TRACKED or
        gazedata.tracking_status == TOBIIGAZE_TRACKING_STATUS_ONE_EYE_TRACKED_PROBABLY_LEFT):
        print("[ %7.4f , %7.4f ] " % (gazedata.left.gaze_point_on_display_normalized.x, 
              gazedata.left.gaze_point_on_display_normalized.y), end="")
        lefteye = "[ %7.4f , %7.4f ] " % (gazedata.left.gaze_point_on_display_normalized.x, 
            gazedata.left.gaze_point_on_display_normalized.y) 
        eye_data_left.append(lefteye)
    
    else:
        print("[ %7s , %7s ] " % ("-", "-"), end="")
        lefteye = "[ %7s , %7s ] " % ("-", "-")
        eye_data_left.append(lefteye)
        
    if (gazedata.tracking_status == TOBIIGAZE_TRACKING_STATUS_BOTH_EYES_TRACKED or
        gazedata.tracking_status == TOBIIGAZE_TRACKING_STATUS_ONLY_RIGHT_EYE_TRACKED or
        gazedata.tracking_status == TOBIIGAZE_TRACKING_STATUS_ONE_EYE_TRACKED_PROBABLY_RIGHT):
        print("[ %7.4f , %7.4f ] " % (gazedata.right.gaze_point_on_display_normalized.x, 
              gazedata.right.gaze_point_on_display_normalized.y), end="")
        righteye = "[ %7.4f , %7.4f ] " % (gazedata.right.gaze_point_on_display_normalized.x, 
            gazedata.right.gaze_point_on_display_normalized.y)
        eye_data_right.append(righteye)
    
    else:
        print("[ %7s , %7s ] " % ("-", "-"), end="")
        righteye = "[ %7s , %7s ] " % ("-", "-")
        eye_data_right.append(righteye)
    
    print("")
    return 0
    
#Data structures to pass to on_gaze_data
tobiiGazeCore64 = WinDLL(os.getcwd() + '\\tobii_lib\\TobiiGazeCore64.dll');
tobiiGazeCore64.tobiigaze_get_connected_eye_tracker(url, URL_SIZE, 
                                                    None)    
eye_tracker = c_void_p(tobiiGazeCore64.tobiigaze_create(url, None))
info = TobiiDeviceInfo()
tobiiGazeCore64.tobiigaze_run_event_loop_on_internal_thread(eye_tracker, 
                                                                None, 
                                                                None)
tobiiGazeCore64.tobiigaze_connect(eye_tracker, byref(errcode))  

print("Connect status: %s" % errcode) 
tobiiGazeCore64.tobiigaze_get_device_info(eye_tracker, byref(info), 
                                          byref(errcode));

tobiigaze_gaze_data_ref = byref(TobiiGazeData())

tobiigaze_gaze_data_extensions_ref= byref(TobiiGazeDataExtensions())

callback_type = WINFUNCTYPE(c_int, POINTER(TobiiGazeData), 
                            POINTER(TobiiGazeDataExtensions),
                            c_void_p)

tobiigaze_start_tracking = tobiiGazeCore64.tobiigaze_start_tracking

tobiigaze_start_tracking.restype = None

tobiigaze_start_tracking.argtypes = (c_void_p, callback_type, 
                                     c_void_p, c_void_p) 
on_gaze_data_func = callback_type(on_gaze_data)

#stored eye_data
eye_data_left = []
eye_data_right = []

def start_tracking():
    
    tobiigaze_start_tracking(eye_tracker, on_gaze_data_func, byref(errcode), 
                             None)                                                        
    
def stop_tracking():
    
    tobiiGazeCore64.tobiigaze_stop_tracking(eye_tracker, byref(errcode))
    tobiiGazeCore64.tobiigaze_disconnect(eye_tracker)
    
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False
    
def clearData():
    del eye_data_left[:]
    del eye_data_right[:]

def plot_eye_data(eye_data_left, eye_data_right, left_color, right_color):
    left_x_float = array.array('f', xrange(0, eye_data_left.__len__()))
    left_y_float = array.array('f', xrange(0, eye_data_left.__len__()))
    right_x_float = array.array('f', xrange(0, eye_data_right.__len__()))
    right_y_float = array.array('f', xrange(0, eye_data_right.__len__()))

    for i in range(0, eye_data_left.__len__()):
        string = ((eye_data_left[i].split(" ")[2]))
        if isfloat(string):
            left_x_float[i] = float(string) * 1.77
        else:
            left_x_float[i] = 0
    for i in range(0, eye_data_left.__len__()):
        string = ((eye_data_left[i].split(" ")[5]))
        if isfloat(string):
            left_y_float[i] = 1 - float(string) 
        else:
            left_y_float[i] = 0
            
    for i in range(0, eye_data_right.__len__()):
        string = ((eye_data_right[i].split(" ")[2]))
        if isfloat(string):
            right_x_float[i] = float(string) * 1.77
        else:
            right_x_float[i] = 0
    for i in range(0, eye_data_right.__len__()):
        string = ((eye_data_right[i].split(" ")[5]))
        if isfloat(string):
            right_y_float[i] = 1 - float(string)
        else:
            right_y_float[i] = 0

    
    im = plt.imread('beach.png')
    plt.imshow(im, zorder=0, extent=[0, 1.777, 0, 1])
    plt.plot(left_x_float,left_y_float, left_color + 'o')
    plt.plot(right_x_float,right_y_float, right_color + 'o')
    #mng = plt.get_current_fig_manager()
    #.window.geometry("1920x1080")
    plt.show()
    
def grab_x():
    string = ((eye_data_left.pop().split(" ")[2]))
    if isfloat(string):
        return float(string) 
    else:
        return 0
            
def grab_y():
    string = ((eye_data_left.pop().split(" ")[5]))
    if isfloat(string):
        return  float(string) 
    else:
        return 0

    
    

    
