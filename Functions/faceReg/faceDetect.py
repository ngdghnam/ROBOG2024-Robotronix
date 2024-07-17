import detector
import YanAPI
YanAPI.yan_api_init("192.168.0.160")
import cv2

def screenshot(Gemni: bool) -> str: 
    """
    This function is used to take a photo from the robot's current vision and return the name of the person it recognizes. 
    """
    YanAPI.sync_do_tts("Please look at me so I can see you and wait 5 seconds")
    vidcap = cv2.VideoCapture('http://192.168.0.160:8000/stream.mjpg')
    success,image = vidcap.read()
    cv2.imwrite("frame.jpg", image) # save frame as JPEG file      
    success,image = vidcap.read()
    print('Read a new frame: ', success)
    
    return
