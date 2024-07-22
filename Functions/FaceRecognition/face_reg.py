import detector
import sys
import os
import YanAPI
import random
import string
sys.path.append(os.path.abspath('.'))
import config
ip_addr = config.YanIP
YanAPI.yan_api_init(ip_addr)

sys.path.append(os.path.abspath('./Functions/TakePicture'))
from take_picture import screenshot # type: ignore


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
        for i in range(0, 20):
            os.rename(f'./Functions/TakePicture/screenshot/screenshot{i}.jpg', f'./Functions/FaceRecognition/training/{name}/screenshot{i}.jpg')
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
    result = detector.recognize_faces(image_location='./Functions/TakePicure/screenshot/screenshot0.jpg')
    os.remove("./Functions/TakePicure/screenshot/screenshot0.jpg")
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
            os.rename(f'./Functions/TakePicure/screenshot/screenshot{i}.jpg', f'./Functions/FaceRecognition/training/{name}/screenshot{code}.jpg')
        detector.encode_known_faces(model='cnn')
        return 0
    except:
        return 2
    else:
        return 1

if __name__ == "__main__":
    # face_registration("nam")
    face_registration('Nam')
    # face_recognition()