# AI-virtual-mouse
This project implements a fully functional AI-based Virtual Mouse that uses your webcam to detect and track hand gestures for controlling the mouse pointer — without touching any physical device. Built using OpenCV, MediaPipe, and PyAutoGUI, this system replaces traditional mouse input with real-time hand tracking and gesture recognition.

🔧 Features
Cursor Movement: Move your index finger and thumb apart, and the cursor follows your hand position accurately on the screen.

Left Click: Bring index finger and thumb together (pinch gesture) to perform a left-click.

Right Click: Touch middle finger and thumb to trigger a right-click event.

Scrolling: Show index and middle finger straight (vertical “peace sign”) to scroll up/down.

Drag and Drop: Close your fist to drag an item and release the fist to drop it.

Highly Stable and Smooth Tracking with filters and interpolation for real-time usability.

🧠 Technologies Used
Python 3

OpenCV – for webcam video capture and image processing

MediaPipe – for accurate and fast hand landmark detection

PyAutoGUI – for controlling mouse events and scrolling

🚀 How It Works
Accesses your webcam feed.

Uses MediaPipe to detect hand landmarks and track specific finger tips.

Based on hand pose and gesture logic, maps movements and gestures to mouse actions.

Ensures stability and responsiveness with smoothing techniques.

📦 Use Cases
Touchless interaction for hygiene-sensitive environments

Experimental AI-HCI applications

Creative tech projects and virtual user interfaces

🖥️ Requirements
Python 3.7+

OpenCV

MediaPipe

PyAutoGUI
