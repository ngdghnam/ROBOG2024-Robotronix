# Import libraries
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append(os.path.abspath('./Functions/FaceRecognition'))
from face_reg import screenshot # type: ignore

classFile  = "./Functions/ObjectDetect/coco_class_labels.txt"

with open(classFile) as fp:
    labels = fp.read().split("\n")
    
# print(labels)

modelFile  = os.path.join("./Functions/ObjectDetect/models", "ssd_mobilenet_v2_coco_2018_03_29", "frozen_inference_graph.pb")
configFile = os.path.join("./Functions/ObjectDetect/models", "ssd_mobilenet_v2_coco_2018_03_29.pbtxt")

# Read the Tensorflow network
net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

# For ach file in the directory
def detect_objects(net, im, dim = 300):

    # Create a blob from the image
    blob = cv2.dnn.blobFromImage(im, 1.0, size=(dim, dim), mean=(0, 0, 0), swapRB=True, crop=False)

    # Pass blob to the network
    net.setInput(blob)

    # Peform Prediction
    objects = net.forward()
    return objects

FONTFACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
THICKNESS = 1

def display_text(im, text, x, y):
    # Get text size
    textSize = cv2.getTextSize(text, FONTFACE, FONT_SCALE, THICKNESS)
    dim = textSize[0]
    baseline = textSize[1]

    # Use text size to create a black rectangle
    cv2.rectangle(
        im,
        (x, y - dim[1] - baseline),
        (x + dim[0], y + baseline),
        (0, 0, 0),
        cv2.FILLED,
    )

    # Display text inside the rectangle
    cv2.putText(
        im,
        text,
        (x, y - 5),
        FONTFACE,
        FONT_SCALE,
        (0, 0, 255),
        THICKNESS,
        cv2.LINE_AA,
    )

def display_objects(im, objects, threshold=0.3):
    rows = im.shape[0]
    cols = im.shape[1]
    object_list=[]

    # For every Detected Object
    for i in range(objects.shape[2]):
        # Find the class and confidence
        classId = int(objects[0, 0, i, 1])
        score = float(objects[0, 0, i, 2])

        # Recover original cordinates from normalized coordinates
        x = int(objects[0, 0, i, 3] * cols)
        y = int(objects[0, 0, i, 4] * rows)
        w = int(objects[0, 0, i, 5] * cols - x)
        h = int(objects[0, 0, i, 6] * rows - y)

        # Check if the detection is of good quality
        if score > threshold:
            label = labels[classId] if labels is not None else f'Class {classId}'
            display_text(im, "{}".format(label), x, y)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 0), 2)
            object_list.append(label)

    # Convert Image to RGB since we are using Matplotlib for displaying image
    """
    mp_img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(30, 10))
    plt.imshow(mp_img)
    plt.show()
    """
    return object_list

def detect_obj(Gemini: bool=True) -> list:
    """
    Take a picture and detect objects in it

    argument:
    - Gemini: check if Gemini is calling the function

    return:
    - a list of objects name
    """
    print("System: Running Object Detection")
    screenshot(1)
    os.rename(f'./Functions/FaceRecognition/screenshot/screenshot0.jpg', f'./Functions/ObjectDetect/images/screenshot.jpg')
    im = cv2.imread(os.path.join("./Functions/ObjectDetect/images", "screenshot.jpg"))
    objects = detect_objects(net, im)
    result = display_objects(im, objects)
    os.remove("./Functions/ObjectDetect/images/screenshot.jpg")

    return result