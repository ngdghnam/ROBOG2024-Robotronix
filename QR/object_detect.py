from ultralytics import YOLO 
from enum import Enum

class ModelType(Enum):
    YOLOv8n = 'yolov8n.pt'
    YOLOv8n = 'yolov8s.pt'
    YOLOv8n = 'yolov8x.pt'

class Camera(Enum):
    LOGI_1 = '0'
    LAPTOP = '1'
    LOGI_2 = '2'

def LiveObjectDetection(modelType:ModelType):
    model = YOLO(modelType.value)
    model.predict(source=Camera.LAPTOP.value, show=True)

if __name__ == '__main__':
    LiveObjectDetection(ModelType.YOLOv8n)
    