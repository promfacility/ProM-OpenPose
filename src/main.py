# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import configparser

try:
    import pyopenpose as op
except ImportError as e:
    print(
        'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

config = configparser.ConfigParser()
config.read('../config.ini')

params = dict()
params["model_folder"] = config['general']['model_folder']

WINDOW_NAME = config['general']['window_name']
WIDTH = int(config['general']['width'])
HEIGHT = int(config['general']['height'])



def open_cam_onboard(WIDTH, HEIGHT):
    # On versions of L4T prior to 28.1, add 'flip-method=2' into gst_str
    gst_str = ('nvcamerasrc ! '
               'video/x-raw(memory:NVMM), '
               'width=(int)2592, height=(int)1458, '
               'format=(string)I420, framerate=(fraction)30/1 ! '
               'nvvidconv ! '
               'video/x-raw, width=(int){}, height=(int){}, '
               'format=(string)BGRx ! '
               'videoconvert ! appsink').format(WIDTH, HEIGHT)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)


# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

# Videocapture
streamer = open_cam_onboard(WIDTH, HEIGHT)

while True:
    _, imageToProcess = streamer.read()  # grab the next image frame from camera
    datum = op.Datum()

    datum.cvInputData = imageToProcess
    opWrapper.emplaceAndPop([datum])

    # Display Image
    cv2.imshow(WINDOW_NAME, datum.cvOutputData)
    key = cv2.waitKey(10)
    if key == 27:  # Check for ESC key
        cv2.destroyAllWindows()
        break


