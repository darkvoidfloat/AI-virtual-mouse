import cv2
import mediapipe as mp
import pyautogui
import numpy as np
from collections import deque

# Initialize
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

# Gesture flags
clicking = False
right_clicking = False
dragging = False
scroll_y_prev = None

# Smoothing buffer
cursor_smoothing_buffer = deque(maxlen=5)

def get_landmark_px(hand_landmarks, index, frame_w, frame_h):
    lm = hand_landmarks.landmark[index]
    return int(lm.x * frame_w), int(lm.y * frame_h)

def distance(pt1, pt2):
    return np.hypot(pt1[0] - pt2[0], pt1[1] - pt2[1])

def smooth_cursor(x, y):
    cursor_smoothing_buffer.append((x, y))
    avg_x = int(np.mean([pt[0] for pt in cursor_smoothing_buffer]))
    avg_y = int(np.mean([pt[1] for pt in cursor_smoothing_buffer]))
    return avg_x, avg_y

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            # Landmark points
            index_tip = get_landmark_px(handLms, 8, w, h)
            thumb_tip = get_landmark_px(handLms, 4, w, h)
            middle_tip = get_landmark_px(handLms, 12, w, h)

            screen_x = int(handLms.landmark[8].x * screen_w)
            screen_y = int(handLms.landmark[8].y * screen_h)

            # Smooth the cursor
            smoothed_x, smoothed_y = smooth_cursor(screen_x, screen_y)

            # Move cursor if fingers apart
            index_up = handLms.landmark[8].y < handLms.landmark[6].y
            thumb_apart = abs(handLms.landmark[4].x - handLms.landmark[8].x) > 0.06
            if index_up and thumb_apart and not dragging:
                pyautogui.moveTo(smoothed_x, smoothed_y)

            # Left click
            if distance(index_tip, thumb_tip) < 30:
                if not clicking:
                    clicking = True
                    pyautogui.click()
            else:
                clicking = False

            # Right click
            if distance(middle_tip, thumb_tip) < 30:
                if not right_clicking:
                    right_clicking = True
                    pyautogui.rightClick()
            else:
                right_clicking = False

            # Drag and drop
            if distance(index_tip, thumb_tip) < 30:
                if not dragging:
                    dragging = True
                    pyautogui.mouseDown()
            elif dragging:
                dragging = False
                pyautogui.mouseUp()

            # Scroll
            index_up = handLms.landmark[8].y < handLms.landmark[6].y
            middle_up = handLms.landmark[12].y < handLms.landmark[10].y
            if index_up and middle_up:
                current_scroll_y = handLms.landmark[8].y
                if scroll_y_prev is not None:
                    diff = scroll_y_prev - current_scroll_y
                    pyautogui.scroll(int(diff * 1000))
                scroll_y_prev = current_scroll_y
            else:
                scroll_y_prev = None

            # Show cursor dot
            cv2.circle(frame, index_tip, 10, (0, 255, 0), -1)

    cv2.imshow("Stable Virtual Mouse", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
