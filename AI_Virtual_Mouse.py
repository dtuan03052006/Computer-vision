

import cv2
import Hand_tracking as htm
import time
import autopy
import numpy as np
import math

wCam, hCam = 640, 480
frameR = 100
smoothing =0.7
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector= htm.handDetector()
wscr,hscr=autopy.screen.size()
pTime=0
clicking = False
while(1):
    sucess,img=cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    cv2.rectangle(
        img,
        (frameR, frameR),
        (wCam - frameR, hCam - frameR),
        (255, 0, 255),
        2
    )
    if(len(lmList)):
        fingers=detector.fingersUp()
        x1,y1=lmList[8][1:]
        if fingers[1] == 1 and fingers[2] == 0:
            x3=np.interp(x1,(frameR,wCam-frameR),(0,wscr))
            y3=np.interp(y1,(frameR,hCam-frameR),(0,hscr))


            autopy.mouse.move(x3,y3)
            cv2.circle(
                img,
                (x1, y1),
                15,
                (255, 0, 255),
                cv2.FILLED
            )
        if(fingers[1]==1 and fingers[2]==1):
            length,img,lineinfor = detector.findDistance(8,12,img)
            if length < 40:
                cv2.circle(
                    img,
                    (lineinfor[4], lineinfor[5]),
                    15,
                    (0, 255, 0),
                    cv2.FILLED
                )
                if not clicking:
                    autopy.mouse.click()
                    clicking = True
            else:
                clicking = False
        else:
            clicking = False
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)