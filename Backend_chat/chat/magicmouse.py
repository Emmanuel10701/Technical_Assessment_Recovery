import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import os
import time
import speech_recognition as sr
import pyttsx3

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Screen width and height
screen_width, screen_height = pyautogui.size()

# Voice assistant setup
engine = pyttsx3.init()

# Function to open applications
def open_app(app_name):
    if "notepad" in app_name:
        os.system("notepad")
    elif "chrome" in app_name:
        os.system("start chrome")
    elif "file explorer" in app_name:
        os.system("explorer")
    elif "command prompt" in app_name:
        os.system("cmd")
    else:
        speak(f"Application {app_name} not found.")

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice commands
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Command: {command}")
        return command
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

# Store last click time for double-click detection
last_click_time = 0

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get index finger and thumb positions
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Convert to screen coordinates
            x = int(index_tip.x * screen_width)
            y = int(index_tip.y * screen_height)

            # Move mouse
            pyautogui.moveTo(x, y)

            # Calculate distance between thumb and index finger
            distance = np.linalg.norm(
                np.array([index_tip.x, index_tip.y]) -
                np.array([thumb_tip.x, thumb_tip.y])
            )

            # Click if fingers are close
            if distance < 0.05:
                current_time = time.time()
                if current_time - last_click_time < 0.3:  # Double-tap
                    pyautogui.doubleClick()
                    print("Double Clicked!")
                else:
                    pyautogui.click()
                    print("Single Clicked!")
                
                last_click_time = current_time  # Update last click time

            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show webcam feed
    cv2.imshow("Hand Control System", frame)

    # Listen for voice command
    command = listen_command()
    if command:
        open_app(command)  # Open application with voice

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
