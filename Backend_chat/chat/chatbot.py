import cv2
import mediapipe as mp

# Initialize Mediapipe Hand Tracking
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Open camera
cap = cv2.VideoCapture(0)

# Get screen width (used for left/center/right detection)
screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

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

        # If hands are detected
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get hand position (center of the palm)
                palm_x = hand_landmarks.landmark[0].x * screen_width  # Normalize to screen width
                
                # Determine hand movement (Left, Center, Right)
                if palm_x < screen_width * 0.3:
                    hand_position = "Left"
                elif palm_x > screen_width * 0.7:
                    hand_position = "Right"
                else:
                    hand_position = "Center"

                # Get finger tip positions
                finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky tips
                thumb_tip = 4

                fingers_up = []
                finger_names = ["Index", "Middle", "Ring", "Pinky"]
                raised_fingers = []

                for i, tip in enumerate(finger_tips):
                    # Compare the y-coordinates of the tip and lower joint (knuckle)
                    if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                        fingers_up.append(True)
                        raised_fingers.append(finger_names[i])
                    else:
                        fingers_up.append(False)

                # Thumb detection (Check if it's pointing outward)
                if hand_landmarks.landmark[thumb_tip].x > hand_landmarks.landmark[thumb_tip - 1].x:
                    fingers_up.append(True)
                    raised_fingers.append("Thumb")
                else:
                    fingers_up.append(False)

                # Create status message
                if raised_fingers:
                    status = "Raised: " + ", ".join(raised_fingers)
                else:
                    status = "No Fingers Raised"

                # Display status on screen
                cv2.putText(frame, status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.putText(frame, f"Hand Position: {hand_position}", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # Show the frame
        cv2.imshow("Finger Detection & Hand Tracking", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
