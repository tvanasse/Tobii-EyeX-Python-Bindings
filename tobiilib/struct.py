from __future__ import print_function
from ctypes import *
import array 
import numpy as np
import matplotlib.pyplot as plt



URLsize = c_uint32(256);
url = create_string_buffer(256);
errcode = c_uint32()

class tobii_device_info(Structure):
    _fields_ =[("serial_number", c_char * 128), ("model", c_char * 64),
               ("generation", c_char * 64), ("firmware_version", c_char * 128)]

#Data structure for Async Minmal Eye Tracking
    
class LIST_ENTRY(Structure):
    pass
LIST_ENTRY._fields_ = [
        ("Flink",   c_void_p),     # POINTER(LIST_ENTRY)
        ("Blink",   c_void_p),     # POINTER(LIST_ENTRY)
]

class RTL_CRITICAL_SECTION(Structure):
    _pack_ = 1
class RTL_CRITICAL_SECTION_DEBUG(Structure):
    _pack_ = 1
##PRTL_CRITICAL_SECTION       = POINTER(RTL_CRITICAL_SECTION)
##PRTL_CRITICAL_SECTION_DEBUG = POINTER(RTL_CRITICAL_SECTION_DEBUG)
PRTL_CRITICAL_SECTION       = c_void_p
PRTL_CRITICAL_SECTION_DEBUG = c_void_p
RTL_CRITICAL_SECTION._fields_ = [
        ("DebugInfo",       PRTL_CRITICAL_SECTION_DEBUG),
        ("LockCount",       c_long),
        ("RecursionCount",  c_long),
        ("OwningThread",    c_void_p),
        ("LockSemaphore",   c_void_p),
        ("SpinCount",       POINTER(c_long)),
]
RTL_CRITICAL_SECTION_DEBUG._fields_ = [
        ("Type",                        c_ushort),
        ("CreatorBackTraceIndex",       c_ushort),
        ("CriticalSection",             PRTL_CRITICAL_SECTION),
        ("ProcessLocksList",            LIST_ENTRY),
        ("EntryCount",                  c_ulong),
        ("ContentionCount",             c_ulong),
        ("Flags",                       c_ulong),
        ("CreatorBackTraceIndexHigh",   c_ushort),
        ("SpareUSHORT",                 c_ushort),
]

class xcondition_variable(Structure):
    _fields_ = [
                ("cs", RTL_CRITICAL_SECTION),
                ("cv", c_void_p),
                ("ready", c_int)
                ]


##class _RTL_CRITICAL_SECTION(Structure):
##    _fields_ = [("LockCount", c_long), ("RecursionCount", c_long), 
##                ("OwningThread", c_void_p), ("LockSemaphore", c_void_p),
##                ("SpinCount", POINTER(c_long), ("DebugInfo", PRTL_CRITICAL_SECTION_DEBUG)) ]
##
##class _RFL_CRITICAL_SECTION_DEBUG:
##    _fields_ = [("Type", c_ushort), ("CreatorBackTraceIndex", c_ushort),
##                ("ProcessLocksList", )
##                
##class _RTL_CRITICAL_SECTION_DEBUG:
##    _fields_ = [("Type", c_ushort), ("CreatorBackTraceIndex", c_ushort),
##                ("CriticalSection", POINTER(_RTL_CRITICAL_SECTION)), ("EntryCount", c_ulong), ("ContentionCount", c_ulong]
##                ("Flags", c_ulong), ("CreatorBackTraceIndexHigh", c_ushort), ("SpareWORD", c_ushort)]


#Data structures to pass to on_gaze_data
TOBIIGAZE_TRACKING_STATUS_NO_EYES_TRACKED = 0
TOBIIGAZE_TRACKING_STATUS_BOTH_EYES_TRACKED = 1
TOBIIGAZE_TRACKING_STATUS_ONLY_LEFT_EYE_TRACKED = 2
TOBIIGAZE_TRACKING_STATUS_ONE_EYE_TRACKED_PROBABLY_LEFT = 3
TOBIIGAZE_TRACKING_STATUS_ONE_EYE_TRACKED_UNKNOWN_WHICH = 4
TOBIIGAZE_TRACKING_STATUS_ONE_EYE_TRACKED_PROBABLY_RIGHT = 5
TOBIIGAZE_TRACKING_STATUS_ONLY_RIGHT_EYE_TRACKED = 6
TOBIIGAZE_MAX_GAZE_DATA_EXTENSIONS = 32

class tobiigaze_point_3d(Structure):
    _fields_ = [("x", c_double), ("y", c_double), ("z", c_double)]

class tobiigaze_point_2d(Structure):
    _fields_ = [("x", c_double), ("y", c_double)]

class tobiigaze_gaze_data_eye(Structure):
    _fields_ = [("eye_position_from_eye_tracker_mm", tobiigaze_point_3d),
                ("eye_position_in_track_box_normalized", tobiigaze_point_3d),
                ("gaze_point_from_eye_tracker_mm", tobiigaze_point_3d),
                ("gaze_point_on_display_normalized", tobiigaze_point_2d)]
    
class tobiigaze_gaze_data(Structure):
    _fields_ = [("timestamp", c_uint64), ("tracking_status", c_uint),
                ("left", tobiigaze_gaze_data_eye), ("right", tobiigaze_gaze_data_eye)]

class tobiigaze_gaze_data_extension(Structure):
    _fields_ = [("column_id", c_uint32), ("data", c_uint8 * 256), ("actual_size", c_uint32)]


class tobiigaze_gaze_data_extensions(Structure):
    _fields_ = [("extensions", tobiigaze_gaze_data_extension * TOBIIGAZE_MAX_GAZE_DATA_EXTENSIONS), ("actual_size", c_uint32)]


#My own created sctructures
user_data = c_void_p()
tobiigaze_gaze_data_ref = byref(tobiigaze_gaze_data())
tobiigaze_gaze_data_extensions_ref = byref(tobiigaze_gaze_data_extensions())
eye_data_left = []
eye_data_right = []

def on_gaze_data(tobiigaze_gaze_data_ref, tobiigaze_gaze_data_extensions_ref, user_data):
    gazedata = tobiigaze_gaze_data_ref.contents
    print("%20.3f " % (gazedata.timestamp / 1e6), end = "") #in seconds
    print("%d " % gazedata.tracking_status, end = "")
       

    if (gazedata.tracking_status == TOBIIGAZE_TRACKING_STATUS_BOTH_EYES_TRACKED or
        gazedata.tracking_status == TOBIIGAZE_TRACKING_STATUS_ONLY_LEFT_EYE_TRACKED or
        gazedata.tracking_status == TOBIIGAZE_TRACKING_STATUS_ONE_EYE_TRACKED_PROBABLY_LEFT):
        print("[ %7.4f , %7.4f ] " % (gazedata.left.gaze_point_on_display_normalized.x, gazedata.left.gaze_point_on_display_normalized.y), end="")
        lefteye = "[ %7.4f , %7.4f ] " % (gazedata.left.gaze_point_on_display_normalized.x, gazedata.left.gaze_point_on_display_normalized.y) 
        eye_data_left.append(lefteye)
    
    else:
        print("[ %7s , %7s ] " % ("-", "-"), end="")
        lefteye = "[ %7s , %7s ] " % ("-", "-")
        eye_data_left.append(lefteye)
        
    

    if (gazedata.tracking_status == TOBIIGAZE_TRACKING_STATUS_BOTH_EYES_TRACKED or
        gazedata.tracking_status == TOBIIGAZE_TRACKING_STATUS_ONLY_RIGHT_EYE_TRACKED or
        gazedata.tracking_status == TOBIIGAZE_TRACKING_STATUS_ONE_EYE_TRACKED_PROBABLY_RIGHT):
        print("[ %7.4f , %7.4f ] " % (gazedata.right.gaze_point_on_display_normalized.x, gazedata.right.gaze_point_on_display_normalized.y), end="")
        righteye = "[ %7.4f , %7.4f ] " % (gazedata.right.gaze_point_on_display_normalized.x, gazedata.right.gaze_point_on_display_normalized.y)
        eye_data_right.append(righteye)
    
    else:
        print("[ %7s , %7s ] " % ("-", "-"), end="")
        righteye = "[ %7s , %7s ] " % ("-", "-")
        eye_data_right.append(righteye)
    

    print("")
    return 0
    
    
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

    
    

    
