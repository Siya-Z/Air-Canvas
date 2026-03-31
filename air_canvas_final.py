import cv2
import numpy as np
import mediapipe as mp
import time

# Initialize MediaPipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Canvas
canvas = np.zeros((480, 640, 3), dtype=np.uint8)

# Colors (BGR)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]  # Last = eraser
colorIndex = 0

xp, yp = 0, 0

# FPS
pTime = 0

def fingers_up(hand):
    fingers = []

    # Index
    if hand.landmark[8].y < hand.landmark[6].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    tips = [12, 16, 20]
    for tip in tips:
        if hand.landmark[tip].y < hand.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Draw UI buttons
    cv2.rectangle(img, (0, 0), (640, 50), (50, 50, 50), -1)

    cv2.putText(img, "BLUE", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
    cv2.putText(img, "GREEN", (120, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    cv2.putText(img, "RED", (240, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    cv2.putText(img, "ERASE", (360, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    cv2.putText(img, "CLEAR", (480, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:

            lmList = []
            h, w, c = img.shape

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((cx, cy))

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            if lmList:
                x1, y1 = lmList[8]

                fingers = fingers_up(handLms)

                # Selection Mode (2 fingers)
                if fingers == [1, 1, 0, 0]:
                    xp, yp = 0, 0

                    if y1 < 50:
                        if 0 < x1 < 100:
                            colorIndex = 0
                        elif 100 < x1 < 200:
                            colorIndex = 1
                        elif 200 < x1 < 300:
                            colorIndex = 2
                        elif 300 < x1 < 400:
                            colorIndex = 3
                        elif 400 < x1 < 640:
                            canvas = np.zeros((480, 640, 3), dtype=np.uint8)

                # Drawing Mode (only index)
                elif fingers == [1, 0, 0, 0]:

                    cv2.circle(img, (x1, y1), 8, colors[colorIndex], cv2.FILLED)

                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    thickness = 15 if colorIndex == 3 else 5
                    cv2.line(canvas, (xp, yp), (x1, y1), colors[colorIndex], thickness)

                    xp, yp = x1, y1

                else:
                    xp, yp = 0, 0

    # Merge canvas
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, inv)
    img = cv2.bitwise_or(img, canvas)

    # FPS
    cTime = time.time()
    fps = int(1/(cTime-pTime)) if (cTime-pTime)!=0 else 0
    pTime = cTime

    cv2.putText(img, f'FPS: {fps}', (10, 470),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.imshow("Air Canvas", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()