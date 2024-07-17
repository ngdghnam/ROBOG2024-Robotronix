import detector
import cv2
import sys
import os
import time
import YanAPI
sys.path.append(os.path.abspath('.'))
import config
ip_addr = config.YanIP
YanAPI.yan_api_init(ip_addr)

def screenshot(gemini: bool) -> bool: 
    """
    This function is used to take a photo from the robot's current vision and return the name of the person it recognizes.

    argument:
    - gemini: check if Gemini is calling the function 
    """
    YanAPI.open_vision_stream(resolution='1920x1080')
    
    YanAPI.sync_do_tts("Please look at me so I can see you, wait 5 seconds")
    time.sleep(3)
    vidcap = cv2.VideoCapture('http://192.168.0.160:8000/stream.mjpg')
    image = vidcap.read()
    cv2.imwrite("./Function/FaceDectection/screenshot.jpg", image[1]) # save frame as JPEG file  
    
    YanAPI.close_vision_stream()

if __name__ == "__main__":
    screenshot(True)
