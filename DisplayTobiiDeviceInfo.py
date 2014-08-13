import os
from ctypes import *
from tobiilib import struct

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









