import detector
import cv2
import sys
import os
import time
import YanAPI
import random
import string
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
    vidcap = cv2.VideoCapture('http://192.168.0.160:8000/stream.mjpg')
    for i in range (0, num):
        image = vidcap.read()
        print(cv2.imwrite(f"screenshot{i}.jpg", image[1])) # save frame as JPEG file  
        os.rename(f'screenshot{i}.jpg', f'./Functions/FaceRecognition/screenshot/screenshot{i}.jpg')
    YanAPI.close_vision_stream()

def face_registration(name: str) -> int:
    """
    Train face recognition model with the name of the user and pictures taken from camera

    argument:
    - name: name of the user

    return:
    - Return 0 if the registration is successful
    - Return 1 if the user is already existed
    """
    screenshot(20)
    YanAPI.sync_do_tts("Updating your face, please wait")
    try:
        os.makedirs(f'./Functions/FaceRecognition/training/{name}')
    except FileExistsError:
        return 1
    else:
        for i in range(0, 10):
            os.rename(f'./Functions/FaceRecognition/screenshot/screenshot{i}.jpg', f'./Functions/FaceRecognition/training/{name}/screenshot{i}.jpg')
        detector.encode_known_faces()
    return 0

def face_recognition(Gemini: bool = True) -> str:
    """
    description: Return the name of the user that the camera can regconizes

    argument:
    - Gemini: Check if Gemini is calling the function

    return:
    - Return the name of the user, Return "Unknown" if robot cannot recognize the user
    """
    screenshot(1)
    result = detector.recognize_faces(image_location='./Functions/FaceRecognition/screenshot/screenshot0.jpg')
    os.remove("./Functions/FaceRecognition/screenshot/screenshot0.jpg")
    return result

def add_face_data(name: str) -> int:
    """
    Add additional photos to train recognition model with the name of the user and pictures taken from camera

    argument:
    - name: name of the user

    return:
    - Return 0 if the improvement training is successful
    - Return 1 if the user does exist
    - Return 2 if unsuccessful
    """
    screenshot(10)
    YanAPI.sync_do_tts("Updating your face, please wait")
    try:
        os.makedirs(f'./Functions/FaceRecognition/training/{name}')
    except FileExistsError:
        for i in range(0, 10):
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            os.rename(f'./Functions/FaceRecognition/screenshot/screenshot{i}.jpg', f'./Functions/FaceRecognition/training/{name}/screenshot{code}.jpg')
        detector.encode_known_faces()
        return 0
    except:
        return 2
    else:
        return 1

if __name__ == "__main__":
    # face_registration("nam")
    add_face_data('nam')
    face_recognition()