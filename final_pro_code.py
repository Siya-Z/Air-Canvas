import cv2
import numpy as np
import mediapipe as mp
import time

# Initialize MediaPipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

canvas = np.zeros((480, 640, 3), dtype=np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]
colorIndex = 0

xp, yp = 0, 0
brushThickness = 5
smoothening = 5

strokes = []
current_stroke = []

pTime = 0

def fingers_up(hand):
    fingers = []

    # Thumb
    if hand.landmark[4].x > hand.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

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

    # ===== UI BAR =====
    cv2.rectangle(img, (0, 0), (640, 60), (40, 40, 40), -1)

    # Color buttons
    for i, color in enumerate(colors):
        cv2.rectangle(img, (10 + i*80, 10), (70 + i*80, 50), color, -1)
        if i == colorIndex:
            cv2.rectangle(img, (10 + i*80, 10), (70 + i*80, 50), (255,255,255), 2)

    cv2.putText(img, "UNDO", (350, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv2.putText(img, "SAVE", (450, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    cv2.putText(img, "CLEAR", (540, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

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
                totalFingers = fingers.count(1)

                # ===== DRAWING MODE =====
                if totalFingers == 1 and fingers[1] == 1 and y1 > 60:

                    x1 = int((xp + x1) / smoothening)
                    y1 = int((yp + y1) / smoothening)

                    cv2.circle(img, (x1, y1), 8, colors[colorIndex], cv2.FILLED)

                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    thickness = 20 if colorIndex == 3 else brushThickness
                    cv2.line(canvas, (xp, yp), (x1, y1), colors[colorIndex], thickness)

                    current_stroke.append((x1, y1))
                    xp, yp = x1, y1

                # ===== SELECTION MODE =====
                elif totalFingers >= 2 and y1 < 60:

                    xp, yp = 0, 0

                    if len(current_stroke) > 0:
                        strokes.append(current_stroke)
                        current_stroke = []

                    # Color select
                    for i in range(len(colors)):
                        if 10 + i*80 < x1 < 70 + i*80:
                            colorIndex = i

                    # Undo
                    if 330 < x1 < 420 and strokes:
                        strokes.pop()
                        canvas = np.zeros((480, 640, 3), dtype=np.uint8)
                        for stroke in strokes:
                            for i in range(1, len(stroke)):
                                cv2.line(canvas, stroke[i-1], stroke[i], colors[colorIndex], brushThickness)

                    # Save
                    if 430 < x1 < 520:
                        filename = f"drawing_{int(time.time())}.png"
                        cv2.imwrite(filename, canvas)
                        print("Saved:", filename)

                    # Clear
                    if 520 < x1 < 640:
                        canvas = np.zeros((480, 640, 3), dtype=np.uint8)
                        strokes = []

                else:
                    xp, yp = 0, 0

                # ===== BRUSH CONTROL =====
                if fingers[0] == 1:  # Thumb
                    brushThickness = min(20, brushThickness + 1)

                if fingers[4] == 1:  # Pinky
                    brushThickness = max(1, brushThickness - 1)

    # Merge canvas
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, inv)
    img = cv2.bitwise_or(img, canvas)

    # FPS
    cTime = time.time()
    fps = int(1/(cTime - pTime)) if (cTime - pTime) != 0 else 0
    pTime = cTime

    cv2.putText(img, f'FPS: {fps}', (10, 470),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.imshow("Air Canvas PRO", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()