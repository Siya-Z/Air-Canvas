Air Canvas – Virtual Drawing Board
Air Canvas is a computer vision-based virtual drawing application that enables users to draw in the air using hand gestures. Built with OpenCV and MediaPipe, it offers real-time hand tracking, gesture-based controls, color selection, and a touchless, interactive drawing experience.

-Features
1. Real-time hand tracking
2. Draw using index finger
3. Gesture-based color selection
4. Clear canvas option
5. Save drawing as image
6. Smooth and interactive UI

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
git clone https://github.com/your-username/Air-Canvas-Computer-Vision.git
cd Air-Canvas-Computer-Vision
2. Install Dependencies
py -3.10 -m pip install opencv-python mediapipe numpy

-- How to Run
py -3.10 air_canvas_gui.py

-Controls

| Gesture      | Action       |
| ------------ | ------------ |
| Index finger | Draw         |
| Two fingers  | Select mode  |
| Top bar      | Choose color |
| CLEAR button | Clear canvas |
| SAVE button  | Save drawing |

- Output
<img width="956" height="759" alt="Screenshot 2026-03-31 223007" src="https://github.com/user-attachments/assets/e9c62ede-6542-49e8-91e4-62989d81d1dd" />
<img width="956" height="759" alt="image" src="https://github.com/user-attachments/assets/140c0fcf-0f5c-4a93-bbed-8a463f98c28b" />

-How It Works

1. MediaPipe detects hand landmarks
2. Index finger tip is tracked
3. Drawing is done on a virtual canvas
4. Canvas is merged with webcam feed

- Future Improvements

1. Undo feature
2. Brush size control
3. Multi-hand support
4. Advanced GUI

-By Siya
