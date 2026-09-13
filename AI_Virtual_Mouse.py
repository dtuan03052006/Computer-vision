
from pynput.mouse import Controller

import cv2
import Hand_tracking as htm
import time
import autopy
import numpy as np
import math
wCam, hCam = 640, 480
frameR = 100
smoothening = 3
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector= htm.handDetector()
wscr,hscr=autopy.screen.size()
pTime=0
mouse = Controller()
right_clicking= False
clicking = False
prev_y = 0
def move(fingers, x1, y1, img):
    global plocX, plocY
    if fingers[1] == 1 and fingers[2] == 0:
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wscr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hscr))

        if plocX == 0 and plocY == 0: 
            plocX, plocY = x3, y3

        # Làm mịn tọa độ (Smoothening)
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening

        # Giới hạn trong kích thước màn hình để tránh lỗi autopy
        clocX = np.clip(clocX, 0, wscr - 1)
        clocY = np.clip(clocY, 0, hscr - 1)

        autopy.mouse.move(clocX, clocY)
        cv2.circle(
            img,
            (x1, y1),
            15,
            (255, 0, 255),
            cv2.FILLED
        )
        plocX, plocY = clocX, clocY

def click_and_scroll(fingers, y1, img):
    global clicking, prev_y
    if fingers[1] == 1 and fingers[2] == 1:
        length, img, lineinfor = detector.findDistance(8, 12, img)
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
            prev_y = 0
        else:
            clicking = False
            if prev_y != 0: 
                detal_y = y1 - prev_y
                if detal_y < -15:
                    mouse.scroll(0, 2)
                    cv2.putText(img, "SCROLL UP", (50, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                elif detal_y > 15:
                    mouse.scroll(0, -2)
                    cv2.putText(img, "SCROLL DOWN", (50, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            prev_y = y1
    else:
        clicking = False
        prev_y = 0 

def right_click(fingers, img):
    global right_clicking
    if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0:
        length_r, img, lineinfor_r = detector.findDistance(4, 8, img)
        if length_r < 35:
            cv2.circle(
                img,
                (lineinfor_r[4], lineinfor_r[5]),
                15,
                (0, 255, 0),
                cv2.FILLED
            )
            if not right_clicking:
                autopy.mouse.click(autopy.mouse.Button.RIGHT)
                right_clicking = True
        else:
            right_clicking = False
    else:
        right_clicking = False
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
        move(fingers,x1,y1,img)
        click_and_scroll(fingers,y1,img)
        right_click(fingers,img)
    else:
        # Reset khi không thấy tay để khi đưa tay lại không bị lướt con trỏ từ vị trí cũ
        plocX, plocY = 0, 0

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)