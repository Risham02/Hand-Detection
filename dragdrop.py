import cv2
from imutils.video import WebcamVideoStream
from HandTrackingModule import handDetector
import time

cap = WebcamVideoStream(src = 0).start()
detector = handDetector(detectionConfidence=0.8)
colorR = (255,0,255)

cx,cy,w,h = 100,100,200,200

time_start = 0
time_curr = 0

while True:
    img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    colorR = (255,0,255)
    
    if lmList:

        l, _ , _ = detector.findDistance(8,12,img)

        if l<60:
            cursor = lmList[8]
            if cx-w//2<cursor[1]<cx+w//2 and cy-h//2<cursor[2]<cy+h//2:
                colorR = 0,255,0
                cx,cy = cursor[1],cursor[2]

    cv2.rectangle(img,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2),colorR,cv2.FILLED)

    time_curr = time.time()
    fps = 1/(time_curr-time_start)
    time_start = time_curr
    
    cv2.putText(img,str(round(fps,2)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        cap.stop()
        break
