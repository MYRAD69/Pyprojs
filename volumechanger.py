import numpy as np
import cv2
import mediapipe as mp
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.mediapipe.python.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils
pTime = 0
cTime = 0
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            s = handLms.landmark[4]
            c = handLms.landmark[8]
            h, w, p = img.shape
            x1, y1 = int(s.x * w), int(s.y * h)
            x2, y2 = int(c.x * w), int(c.y * h)
            d = int(np.sqrt((s.x - c.x)**2 + (s.y - c.y)**2) * 200)
            if d > 100:
                d = 100
            # print(d)
            
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 3)
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img, (mx, my), 10, (255, 0, 255), cv2.FILLED)
            vol = np.interp(d, [0, 100], [minVol, maxVol])
            print(vol)
            volume.SetMasterVolumeLevel(vol, None)
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)