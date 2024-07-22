import sys
import os
import YanAPI
import time
import cv2
sys.path.append(os.path.abspath('.'))
import config
ip_addr = config.YanIP
YanAPI.yan_api_init(ip_addr)

def screenshot(num: int) -> None: 
    """
    This function is used to take a photo from the robot's current vision and return the name of the person it recognizes.

    argument:
    - num: the number of pictures
    """
    YanAPI.open_vision_stream(resolution='1920x1080')
    
    YanAPI.sync_do_tts("I'm looking in front of me, analysing")
    time.sleep(5)
    vidcap = cv2.VideoCapture('http://{ip}:8000/stream.mjpg'.format(ip=ip_addr))
    for i in range (0, num):
        image = vidcap.read()
        print(cv2.imwrite(f"screenshot{i}.jpg", image[1])) # save frame as JPEG file  
        os.rename(f'screenshot{i}.jpg', f'./Functions/TakePicture/screenshot/screenshot{i}.jpg')
    YanAPI.close_vision_stream()