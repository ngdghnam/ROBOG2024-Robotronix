# Xử lý cầm đồ vật 
import YanAPI  
import time 
import cv2 

def decode_qrcode(qr_code):
    img = cv2.imread(qr_code)
    detector = cv2.QRCodeDetector()

    # detect and decode
    data, bbox, straight_qrcode = detector.detectAndDecode(img)

    # if there is a QR code
    if bbox is not None:
        # print(f"QRCode data: {data}")
        return "QR Code Data: {}".format(data)

# def detect_qrcode_livecam():
#     cap = cv2.VideoCapture(0)
#     detector = cv2.QRCodeDetector()
#     while True:
#         _, img = cap.read()
#         data, bbox, _ = detector.detectAndDecode(img)
#         if bbox is not None: 
#             if data: 
#                 return data 

def processQR():
    res = YanAPI.sync_do_QR_code_recognition()
    val = res["data"]["recognition"]["name"]
    while val != None:
        qr = YanAPI.take_vision_photo()
        result = decode_qrcode(qr) 
        YanAPI.sync_do_tts(result)
    else: 
        YanAPI.sync_do_tts("Cannot detect qr code")

if __name__ == '__main__':
    processQR()
    