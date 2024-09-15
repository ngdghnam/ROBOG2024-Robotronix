import cv2 
import YanAPI

ip_adr = "192.168.68.124"
YanAPI.yan_api_init(ip_adr)

cap = cv2.VideoCapture(0)

while True:
    # savce img in the variable img
    # Success is boolean 
    success, img = cap.read()
    cv2.imshow("Video", img )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

