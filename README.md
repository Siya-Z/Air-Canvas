Air Canvas – Virtual Drawing Board
Air Canvas is a computer vision-based virtual drawing application that enables users to draw in the air using hand gestures. Built with OpenCV and MediaPipe, it offers real-time hand tracking, gesture-based controls, color selection, and a touchless, interactive drawing experience.

-Features
1. Real-time hand tracking
2. Draw using index finger
3. Gesture-based color selection
4. Eraser functionality
5. Adjustable Brush Size
6. Clear canvas option
7. Save drawing as image
8. Smooth and interactive UI

-Technologies Used
1. Python
2. OpenCV
3. MediaPipe
4. NumPy

 Project Structure
AirCanvas/
├── air_canvas_gui.py
├── hand_tracking.py
├── test_camera.py
├── README.md
└── images/


Installation
1. Clone Repository
git clone https://github.com/Siya-Z/Air-Canvas.git
cd Air-Canvas-Computer-Vision
2. Install Dependencies
py -3.10 -m pip install opencv-python mediapipe numpy

-- How to Run
py -3.10 air_canvas_gui.py

-Controls

| Gesture           | Action       |
| ----------------  | ------------ |
| Index finger      | Draw         |
| Two fingers       | Select mode  |
|Increase Brush size| Thumb        |
|Decrease Brush size| Pinky Finger |
|Black Color        | Eraser       |
| Top bar           | Choose color |
| CLEAR button      | Clear canvas |
| SAVE button       | Save drawing |

- Output
<img width="956" height="759" alt="Screenshot 2026-03-31 223007" src="https://github.com/user-attachments/assets/e9c62ede-6542-49e8-91e4-62989d81d1dd" />

-How It Works
MediaPipe detects hand landmarks from the webcam feed. The position of the index finger is tracked and used as a pointer. Drawing is performed on a virtual canvas, which is then combined with the video feed to create the final output.

- Future Improvements
Undo/Redo functionality
Multi-hand support
Advanced gesture recognition
Improved graphical interface

-By Siya
