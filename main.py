import cv2
import mediapipe as mp
import time
from subprocess import call
import numpy as np
from Positions import HandGestureController
##from arduino_manager import ArduinoManager
import math
gestureController = HandGestureController()
time.sleep(2) 
# 1. Initialize Arduino (Defaults to COM5 based on your class)
##arduino = ArduinoManager()
##arduino.connect()


# MediaPipe Setup
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
landmark_style = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4)
connection_style = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2)

VOLUME_UPDATE_INTERVAL = 20

gestureController = HandGestureController()


videoCap = cv2.VideoCapture(0)
lastFrameTime = 0
frame_count = 0
max_diff = 0
min_diff = 100000
lastState = "OFF"


while True:
    frame_count += 1
    success, img = videoCap.read()
   
    if success:
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
       
        thisFrameTime = time.time()
        fps = 1 / (thisFrameTime - lastFrameTime)
        lastFrameTime = thisFrameTime
        cv2.putText(img, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


        results = hands.process(imgRGB)
       
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(
                    img,
                    handLms,
                    mpHands.HAND_CONNECTIONS,
                    landmark_style,
                    connection_style
                )
                if frame_count % VOLUME_UPDATE_INTERVAL == 0:
                    state = gestureController.process(handLms, img.shape)
                    frame_count = 0


        cv2.imshow("CamOutput", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# 4. Clean up connection
#arduino.close()
videoCap.release()
cv2.destroyAllWindows()
