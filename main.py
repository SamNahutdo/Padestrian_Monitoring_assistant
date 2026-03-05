
#e install ni sa git


#pip install python-opencv
#pip install serial
#pip install mediapipe




import cv2
import mediapipe as mp
import serial
import time

# Arduino Setup
time.sleep(2)
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=1)
time.sleep(2)

# Mediapipe Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

def detect_fingers(image, hand_landmarks):
    finger_tips = [8, 12, 16, 20]  
    thumb_tip = 4
    finger_states = [0, 0, 0, 0, 0]  

    # Thumb (left-right)
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        finger_states[0] = 1

    # Other fingers (up-down)
    for idx, tip in enumerate(finger_tips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states[idx + 1] = 1

    return finger_states


# Start capturing video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Hand detection text
    if results.multi_hand_landmarks:
        detection_text = "Hand Detected!"
        detection_color = (0, 255, 0)
    else:
        detection_text = "No Hand Detected"
        detection_color = (0, 0, 255)

    cv2.putText(image, detection_text,
                (image.shape[1]-250, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, detection_color, 2)

    # When a hand is detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers_state = detect_fingers(image, hand_landmarks)
            arduino.write(bytes(fingers_state))
            print(f"Fingers State: {fingers_state}")

            finger_count = sum(fingers_state)

            # Messages for finger counts
            messages = {
                0: "No one manage",
                1: "Warning",
                2: "Slow Down",
                3: "GO",
                4: "Pedestrian Lane Walking",
                5: "STOP"
            }

            # Colors for each message (B, G, R)
            colors = {
                0: (255, 255, 255),   # white
                1: (255, 255, 255),   # white
                2: (0, 255, 255),     # yellow
                3: (0, 255, 0),       # green
                4: (255, 0, 0),       # blue
                5: (0, 0, 255)        # red
            }

            # Pick message and matching color
            text = messages.get(finger_count, "")
            text_color = colors.get(finger_count, (255, 255, 255))

            # Display custom text with color
            cv2.putText(image, text,
                        (image.shape[1]-350, image.shape[0]-20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, text_color, 2)

    # Show camera window
    cv2.imshow('Hand Tracking', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
