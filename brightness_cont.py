import cv2
import mediapipe as mp
import math
import os

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

def set_brightness(level):
    level = max(0, min(100, level))
    os.system(f"brightnessctl set {level}%")

def calculate_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

# Open webcam
cap = cv2.VideoCapture(0)
current_brightness = 50
set_brightness(current_brightness)

print("[*] Move thumb and index apart to change brightness. Press 'q' to quit.")

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get thumb tip and index finger tip coordinates
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]

            h, w, _ = img.shape
            thumb_point = int(thumb_tip.x * w), int(thumb_tip.y * h)
            index_point = int(index_tip.x * w), int(index_tip.y * h)

            # Draw line between fingers
            cv2.line(img, thumb_point, index_point, (0, 255, 0), 3)

            # Calculate distance and map to brightness
            dist = calculate_distance(thumb_point, index_point)

            # Clamp distance (you can fine-tune min/max based on your hand + camera)
            brightness = int((dist - 30) / 150 * 100)  # Range mapping
            brightness = max(0, min(100, brightness))

            if abs(brightness - current_brightness) >= 5:
                current_brightness = brightness
                set_brightness(current_brightness)
                print(f"[+] Brightness set to {current_brightness}%")

    cv2.imshow("Gesture Brightness Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()