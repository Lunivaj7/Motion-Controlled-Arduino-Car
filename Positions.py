import cv2
import mediapipe as mp
import time
from subprocess import call
import numpy as np
##from arduino_manager import ArduinoManager
import math

class HandGestureController:
    def __init__(self):
        self.max_diff = 0
        self.min_diff = 100000
        self.lastState = "OFF"

        self.max_diff2 = 0
        self.min_diff2 = 100000
        self.lastState2 = "GO"

        self.lastState3 = "OFF"

    def process(self, handLms, img_shape):
        h, w, c = img_shape

        self.thumbtip   = (handLms.landmark[4].x*h, handLms.landmark[4].y*h)
        self.indextip   = (handLms.landmark[8].x*h, handLms.landmark[8].y*h)
        self.middletip  = (handLms.landmark[12].x*h, handLms.landmark[12].y*h)
        self.pinkytip   = (handLms.landmark[20].x*h, handLms.landmark[20].y*h)
        self.palmtop    = (handLms.landmark[9].x*h, handLms.landmark[9].y*h)
        self.palmbottom = (handLms.landmark[0].x*h, handLms.landmark[0].y*h)
        self.pinkybottom= (handLms.landmark[17].x*h, handLms.landmark[17].y*h)

        ##To negate Distance effecting measurments
        self.Scale = math.sqrt((self.palmtop[0]-self.palmbottom[0])**2 +(self.palmtop[1]-self.palmbottom[1])**2)
        if self.CheckStop() != "STOP":
            return self.Position_Reverse() , self.tilt()
    

    def CheckStop(self):

        distance = abs(self.middletip[1] - self.palmbottom[1])
        ratiodist = distance/self.Scale
        ###print("Distance:", ratiodist)
        self.min_diff2 = np.minimum(ratiodist, self.min_diff2)
        self.max_diff2 = np.maximum(ratiodist, self.max_diff2)
        # Avoid division by zero
        if  self.max_diff - self.min_diff2 == 0:
            return self.lastState2

        vol = np.clip((ratiodist / (self.max_diff2 - self.min_diff2) * 100), 0, 100)
        
        if int(vol) < 50:
            ###print("Reverse")
            currentState = "STOP"
        else:
            ###print("Reverse")
            currentState = "GO"

        if currentState != self.lastState2:
            print(f"STOP OR GO: {currentState}")
            # send signal to Arduino here if needed
            # arduino.send(currentState)
            self.lastState2 = currentState

        return currentState
    
    def Position_Reverse(self):

        distance = abs(self.thumbtip[0] - self.pinkybottom[0])
        ratiodist = distance/self.Scale
        ###print("Distance:", ratiodist)
        self.min_diff = np.minimum(ratiodist, self.min_diff)
        self.max_diff = np.maximum(ratiodist, self.max_diff)
        # Avoid division by zero
        if  self.max_diff - self.min_diff == 0:
            return self.lastState

        vol = np.clip((ratiodist / (self.max_diff - self.min_diff) * 100), 0, 100)
        
        if int(vol) < 50:
            ###print("Reverse")
            currentState = "REVERSE"
        else:
            ###print("Reverse")
            currentState = "FORWARD"

        if currentState != self.lastState:
            print(f"New Direction: {currentState}")
            # send signal to Arduino here if needed
            # arduino.send(currentState)
            self.lastState = currentState

        return currentState
    def tilt(self):
        tiltrad = math.atan((self.middletip[1]-self.palmbottom[1])/(self.middletip[0]-self.palmbottom[0]))
        Tiltmag = math.degrees(tiltrad)
        if abs(tiltrad) < 1.22:
            if int(self.middletip[0] - self.palmbottom[0]) < 0:
                currentstate2 = "LEFT"
            else:
                currentstate2 = "RIGHT"
        else:
            currentstate2 = "STRAIGHT"


        #chat clutter
        if currentstate2 != self.lastState3:
            print(f"New Direction: {currentstate2}")
            
            # This is where you'd talk to the Arduino
            # self.arduino.send(currentState) 
            
            # 3. Update the memory
            self.lastState3 = currentstate2
        return currentstate2