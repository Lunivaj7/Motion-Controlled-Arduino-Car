import cv2
import mediapipe as mp
import time
from subprocess import call
import numpy as np
import serial
#Use venv: Control + Shift + P: Select Interperter: Python_Project\venv\Scripts\python.exe

# connect to HC-05 module
arduino = serial.Serial('COM3',9600,timeout=0)
time.sleep(2)


# MediaPipe Setup
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)
mpDraw = mp.solutions.drawing_utils
landmark_style = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=3)
connection_style = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2)


fingerTips_ID = [4,8,12,16,20] #[thumb, index, middle, ring, pinky]


#video capture
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

lastFrameTime = 0
frame_count = 0
process_frames = 2
process_data_frames = 10

def get_hand_arr(handLms, img, handType):
    h, w, c = img.shape
    lm = []
    for i in range(21):
        x = int(handLms.landmark[i].x * w)
        y = int(handLms.landmark[i].y * h)
        lm.append((x, y))
    
    #hand array: 1 = open, 0 = closed
    #[thumb, index, middle, ring, pinky]
    hand = [0, 0, 0, 0, 0]


    if (handType=="Right"):
        #Right Thumb
        if lm[4][0] < lm[3][0]-20:
            hand[0]=1
        else:
            hand[0]=0

    else:#Left Thumb
        if lm[4][0] > lm[3][0]+20:
            hand[0]=1
        else:
            hand[0]=0

    #other fingers
    for i, tip in enumerate(fingerTips_ID[1:]):

        if lm[tip][1]<lm[tip-2][1]:
            hand[i+1] = 1
        else:
            hand[i+1] = 0

    return hand

def send(message):
    arduino.write((message + "\n").encode())
    print(message)

#Video Loop
while True:
    success, img = cap.read()
    if not success:
        continue
    
    #flips camera
    img = cv2.flip(img, 1) 
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    #FPS calculation
    thisFrameTime = time.time()
    frame_dif = thisFrameTime - lastFrameTime
    if (frame_dif!=0):
        fps = 1 / (frame_dif)
    else:
        fps = 0
    lastFrameTime = thisFrameTime
    cv2.putText(img, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    frame_count+=1

    #process frames 
    if frame_count % process_frames == 0:

        results = hands.process(imgRGB)
        #hand calculations
        if results.multi_hand_landmarks:
            for handLms, handLabel in zip(results.multi_hand_landmarks, results.multi_handedness):
                mpDraw.draw_landmarks(
                    img, 
                    handLms, 
                    mpHands.HAND_CONNECTIONS,
                    landmark_style,
                    connection_style
                    )

                #get hand array
                if (frame_count%process_data_frames==0):
                    
                    hand_type = handLabel.classification[0].label
                    hand = get_hand_arr(handLms, img, hand_type)    
                    print("Hand Array", hand)

                    if hand==[1,1,1,1,1] or hand == [0,1,1,1,1]:
                        send("FWD")

                    elif hand==[1,0,0,0,0]:
                        send("REV")
            
                    elif (hand==[0,1,0,0,0] and hand_type=="Right") or (hand==[0,0,0,0,1] and hand_type=="Left"):
                        send("LEFT")
            
                    elif (hand==[0,0,0,0,1] and hand_type=="Right") or (hand==[0,1,0,0,0] and hand_type=="Left"):
                        send("RIGHT")
                    else:
                        send("STOP")
        else:
            if frame_count % process_data_frames == 0:
                send("STOP")

            
        #renders camera
        cv2.imshow("Hand Control", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#close connections
arduino.close()
cap.release()
cv2.destroyAllWindows()
