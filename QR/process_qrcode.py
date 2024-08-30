import qrcode 
import cv2 
import os 

# CREATE QR CODE 
def create_qrcode(data):
    qr_code = qrcode.make(data)
    qr_code = qr_code.save("{}.jpg".format(data))
    return qr_code

# create_qrcode(data)
 
# DECODE QR CODE 
"""The detectAndDecode() function takes an image as an input and decodes it to return a tuple of 3 values: 
the data decoded from the QR code, 
the output array of vertices of the found QR code quadrangle, 
and the output image containing rectified and binarized QR code."""
def decode_qrcode(qr_code):
    img = cv2.imread(qr_code)
    detector = cv2.QRCodeDetector()

    # detect and decode
    data, bbox, straight_qrcode = detector.detectAndDecode(img)

    # if there is a QR code
    if bbox is not None:
        # print(f"QRCode data: {data}")
        return "QR Code Data: {}".format(data)

# Detect with live cam 
def detect_qrcode_livecam():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cap.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if bbox is not None: 
            if data: 
                print(data)
                return data 

        cv2.imshow('img', img)
        if cv2.waitKey(1) == ord('q'):
            break 
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # data = input("Command: ")
    # img = create_qrcode(data) 
    detect_qrcode_livecam()
