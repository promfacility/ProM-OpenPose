# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import configparser
#~ import argparse

WINDOW_NAME = "OpenPose 1.4.0 - Tutorial Python API"
def open_cam_onboard(width, height):
    # On versions of L4T prior to 28.1, add 'flip-method=2' into gst_str
    gst_str = ('nvcamerasrc ! '
               'video/x-raw(memory:NVMM), '
               'width=(int)2592, height=(int)1458, '
               'format=(string)I420, framerate=(fraction)30/1 ! '
               'nvvidconv ! '
               'video/x-raw, width=(int){}, height=(int){}, '
               'format=(string)BGRx ! '
               'videoconvert ! appsink').format(width, height)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)


# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.) 
        sys.path.append(dir_path + '/../../python/openpose/Release');
        os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.) 
        #~ sys.path.append('/home/nvidia/openpose/python/openpose');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        import pyopenpose as op
        #~ from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

#~ # Flags
#~ parser = argparse.ArgumentParser()
#~ parser.add_argument("--image_path", default="../../../examples/media/COCO_val2014_000000000192.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
#~ args = parser.parse_known_args()

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "/home/nvidia/openpose/models/"

#~ # Add others in path?
#~ for i in range(0, len(args[1])):
    #~ curr_item = args[1][i]
    #~ if i != len(args[1])-1: next_item = args[1][i+1]
    #~ else: next_item = "1"
    #~ if "--" in curr_item and "--" in next_item:
        #~ key = curr_item.replace('-','')
        #~ if key not in params:  params[key] = "1"
    #~ elif "--" in curr_item and "--" not in next_item:
        #~ key = curr_item.replace('-','')
        #~ if key not in params: params[key] = next_item

# Construct it from system arguments
# op.init_argv(args[1])
# oppython = op.OpenposePython()

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

# Videocapture
streamer = open_cam_onboard(800, 600)

while(1):
	# Process Image
	#~ if cv2.getWindowProperty(WINDOW_NAME, 0) < 0:
		#~ # Check to see if the user has closed the window
		#~ # If yes, terminate the program
		#~ break
	_, imageToProcess = streamer.read() # grab the next image frame from camera
	datum = op.Datum()
	#~ imageToProcess = cv2.imread(args[0].image_path)
	datum.cvInputData = imageToProcess
	opWrapper.emplaceAndPop([datum])

	# Display Image
	#~ print("Body keypoints: \n" + str(datum.poseKeypoints))
	cv2.imshow(WINDOW_NAME, datum.cvOutputData)
	key = cv2.waitKey(10)
	if key == 27: # Check for ESC key
		cv2.destroyAllWindows()
		break ;
