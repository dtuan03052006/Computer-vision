
import cv2
import mediapipe as mp
import time
import math
class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands= mp.solutions.hands  # type: ignore
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils  # type: ignore

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, 
                                               self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self, img, handNo=0, draw=True):
        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
        self.lmList = lmList
        return lmList
    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmList[4][1] < self.lmList[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        if self.lmList[8][2] < self.lmList[7][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Middle
        if self.lmList[12][2] < self.lmList[11][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Ring
        if self.lmList[16][2] < self.lmList[15][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Pinky
        if self.lmList[20][2] < self.lmList[19][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        return fingers
    def findDistance(self,p1,p2,img):
        x1,y1 = self.lmList[p1][1:]
        x2,y2 = self.lmList[p2][1:]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        length=math.hypot(x2-x1,y2-y1)
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        return length,img,[x1,y1,x2,y2,cx,cy]
