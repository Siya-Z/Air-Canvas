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

# 🎨 Pastel Colors + Eraser
colors = [
    (203, 192, 255),  # Light Pink
    (255, 204, 229),  # Light Purple
    (255, 255, 153),  # Light Blue
    (204, 255, 204),  # Light Green
    (0, 0, 0)         # Eraser
]

colorIndex = 0

xp, yp = 0, 0
pTime = 0
brushThickness = 5  # ⭐ Brush size

def fingers_up(hand):
    fingers = []

    # Thumb
    if hand.landmark[4].x > hand.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    tips = [8, 12, 16, 20]
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

    # ===== GUI =====
    cv2.rectangle(img, (0, 0), (640, 60), (40, 40, 40), -1)

    # Color boxes
    for i, color in enumerate(colors):
        cv2.rectangle(img, (10 + i*70, 10), (70 + i*70, 50), color, -1)

        if i == colorIndex:
            cv2.rectangle(img, (10 + i*70, 10), (70 + i*70, 50), (255,255,255), 2)

    # Labels
    cv2.putText(img, "ERASE", (10 + 4*70, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)

    # Clear button
    cv2.rectangle(img, (380, 10), (480, 50), (200,200,200), -1)
    cv2.putText(img, "CLEAR", (385, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)

    # Save button
    cv2.rectangle(img, (500, 10), (620, 50), (180,255,180), -1)
    cv2.putText(img, "SAVE", (515, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)

    # Show brush size
    cv2.putText(img, f'Size: {brushThickness}', (10, 470),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

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

                # ✌️ Selection Mode
                if fingers[1] == 1 and fingers[2] == 1:
                    xp, yp = 0, 0

                    if y1 < 60:
                        # Color select
                        for i in range(len(colors)):
                            if 10 + i*70 < x1 < 70 + i*70:
                                colorIndex = i

                        # Clear
                        if 380 < x1 < 480:
                            canvas = np.zeros((480, 640, 3), dtype=np.uint8)

                        # Save
                        if 500 < x1 < 620:
                            filename = f"drawing_{int(time.time())}.png"
                            cv2.imwrite(filename, canvas)
                            print("Drawing saved!")

                # ☝️ Drawing Mode
                elif fingers[1] == 1 and fingers[2] == 0:

                    cv2.circle(img, (x1, y1), 8, colors[colorIndex], cv2.FILLED)

                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    thickness = 25 if colorIndex == 4 else brushThickness

                    cv2.line(canvas, (xp, yp), (x1, y1),
                             colors[colorIndex], thickness)

                    xp, yp = x1, y1

                else:
                    xp, yp = 0, 0

                # 👍 Increase brush
                if fingers[0] == 1:
                    brushThickness = min(20, brushThickness + 1)

                # 👎 Decrease brush
                if fingers[4] == 1:
                    brushThickness = max(1, brushThickness - 1)

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

    cv2.putText(img, f'FPS: {fps}', (500, 470),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.imshow("Air Canvas", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()