import cv2
import mediapipe as mp
from collections import deque
import numpy as np

# Initialize Mediapipe Hand Tracking
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Open camera
cap = cv2.VideoCapture(0)

# Gesture history for right hand
gesture_history = deque(maxlen=5)

# Hand detection model
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert image to RGB (Mediapipe requires RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image to detect hands
        result = hands.process(rgb_frame)

        # Initialize variables
        right_hand_gesture = "No Gesture"
        left_hand_finger_names = ""
        left_hand_finger_count = 0

        # If hands are detected
        if result.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
                # Get handedness (left or right)
                hand_label = result.multi_handedness[idx].classification[0].label
                is_right_hand = hand_label == "Right"
                is_left_hand = hand_label == "Left"

                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get finger tip positions
                finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky tips
                thumb_tip = 4
                finger_names = ["Index", "Middle", "Ring", "Pinky"]
                
                fingers_up = sum(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y for tip in finger_tips)
                thumb_up = hand_landmarks.landmark[thumb_tip].y < hand_landmarks.landmark[thumb_tip - 1].y
                if thumb_up:
                    fingers_up += 1

                if is_right_hand:
                    # Extended Gesture Recognition
                    if fingers_up == 1 and thumb_up:
                        right_hand_gesture = "👍 Like"
                    elif fingers_up == 0:
                        right_hand_gesture = "✊ Fist"
                    elif fingers_up == 2:
                        right_hand_gesture = "✌️ Peace"
                    elif fingers_up == 3:
                        right_hand_gesture = "🖖 Three Fingers"
                    elif fingers_up == 4:
                        right_hand_gesture = "👌 OK"
                    elif fingers_up == 5:
                        right_hand_gesture = "✋ Stop"
                    elif fingers_up == 1:
                        right_hand_gesture = "👊 Punch"
                    elif fingers_up == 2 and not thumb_up:
                        right_hand_gesture = "🤘 Rock On"
                    elif fingers_up == 1 and thumb_up:
                        right_hand_gesture = "🤙 Call Me"
                    elif fingers_up == 1 and not thumb_up:
                        right_hand_gesture = "🤞🏻 Together"
                    elif fingers_up == 5 and not thumb_up:
                        right_hand_gesture = "🖐🏻 Open Palm"9
                    elif fingers_up == 5 and thumb_up:
                        right_hand_gesture = " Offering"

                    gesture_history.append(right_hand_gesture)

                if is_left_hand:
                    raised_fingers = [finger_names[i] for i, tip in enumerate(finger_tips) if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y]
                    if hand_landmarks.landmark[thumb_tip].y < hand_landmarks.landmark[thumb_tip - 1].y:
                        raised_fingers.append("Thumb")
                    left_hand_finger_names = ", ".join(raised_fingers) if raised_fingers else "No Fingers Raised"
                    left_hand_finger_count = len(raised_fingers)

        # Modern Statistics Display
        overlay = frame.copy()
        cv2.rectangle(overlay, (frame.shape[1] - 310, 10), (frame.shape[1] - 10, 100), (0, 0, 0), -1)
        cv2.rectangle(overlay, (10, frame.shape[0] - 100), (310, frame.shape[0] - 10), (0, 0, 0), -1)
        alpha = 0.6
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        cv2.putText(frame, "Right Hand Stats", (frame.shape[1] - 290, 40), cv2.FONT_HERSHEY_TRIPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"Gesture: {right_hand_gesture}", (frame.shape[1] - 290, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, "Left Hand Stats", (20, frame.shape[0] - 80), cv2.FONT_HERSHEY_TRIPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"Fingers: {left_hand_finger_names} ({left_hand_finger_count})", (20, frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
        cv2.imshow("Hand Gesture Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
