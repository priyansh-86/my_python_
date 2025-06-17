import cv2
import mediapipe as mp
import numpy as np
import os
from collections import deque

# ==== INITIALIZE ====
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.8
)
mp_draw = mp.solutions.drawing_utils

# Buffer to smooth brightness transitions
dist_buffer = deque(maxlen=5)

# === Start webcam ===
cap = cv2.VideoCapture(0)

print("\n[*] Press 'q' to quit.")

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    h, w, _ = img.shape

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            # Get index finger tip and thumb tip
            lm_list = handLms.landmark
            x1, y1 = int(lm_list[4].x * w), int(lm_list[4].y * h)   # Thumb tip
            x2, y2 = int(lm_list[8].x * w), int(lm_list[8].y * h)   # Index tip

            # Draw circle on tips
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)

            # Draw line between fingers
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Calculate distance
            dist = int(np.hypot(x2 - x1, y2 - y1))
            dist_buffer.append(dist)
            avg_dist = sum(dist_buffer) / len(dist_buffer)

            # Map distance (30 to 180) → brightness (0 to 100)
            brightness = np.interp(avg_dist, [30, 180], [0, 100])
            brightness = int(np.clip(brightness, 0, 100))

            # Set brightness (Linux)
            os.system(f"brightnessctl set {brightness}%")

            # Show brightness on screen
            cv2.putText(img, f"Brightness: {brightness}%", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            # Visual bar
            bar_width = int((brightness / 100) * 300)
            cv2.rectangle(img, (10, 70), (310, 100), (255, 255, 255), 2)
            cv2.rectangle(img, (10, 70), (10 + bar_width, 100), (0, 255, 255), cv2.FILLED)

    cv2.imshow("Finger Brightness Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release
cap.release()
cv2.destroyAllWindows()
