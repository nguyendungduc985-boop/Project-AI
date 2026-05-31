import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from PIL import ImageFont, ImageDraw, Image
import math


w_cam, h_cam = 320, 640       
dead_zone = 50                
max_speed = 80               
sensitivity = 0.9            
# Tắt fail-safe
pyautogui.FAILSAFE = False 

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1, 
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)
cap.set(3, w_cam)
cap.set(4, h_cam)

is_dragging = False 
center_cam_x, center_cam_y = w_cam // 2, h_cam // 2

def draw_vietnamese_text(img, text, position, text_color):
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    try:
        font = ImageFont.truetype("arial.ttf", 32) 
    except IOError:
        font = ImageFont.load_default()
    draw.text(position, text, font=font, fill=text_color)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def count_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    fingers_open = 0
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers_open += 1
    for i in range(4):
        if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_pips[i]].y:
            fingers_open += 1
    return fingers_open

print("Chế độ TURBO: Đưa tay ra xa để chuột bay nhanh!")

while True:
    success, img = cap.read()
    if not success: break
    
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    # Vẽ Deadzone
    cv2.circle(img, (center_cam_x, center_cam_y), dead_zone, (255, 0, 255), 2)

    status_text = "..."
    color = (200, 200, 200)
    vx, vy = 0, 0 

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            wrist_x = int(hand_landmarks.landmark[0].x * w_cam)
            wrist_y = int(hand_landmarks.landmark[0].y * h_cam)
            
            cv2.circle(img, (wrist_x, wrist_y), 10, (0, 255, 255), cv2.FILLED)
            cv2.line(img, (center_cam_x, center_cam_y), (wrist_x, wrist_y), (0, 255, 255), 2)

            dx = wrist_x - center_cam_x
            dy = wrist_y - center_cam_y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > dead_zone:

                excess_dist = distance - dead_zone
                
                speed = excess_dist * sensitivity
                
                if excess_dist > 100:
                    speed = speed * 1.5
                speed = min(speed, max_speed)
                
                vx = (dx / distance) * speed
                vy = (dy / distance) * speed

            fingers = count_fingers(hand_landmarks)
            
            if fingers < 2: 
                status_text = "NẮM (Kéo)"
                color = (255, 255, 0)
                if not is_dragging:
                    pyautogui.mouseDown()
                    is_dragging = True
            else:
                status_text = "MỞ (Di chuyển)"
                color = (0, 255, 0)
                if is_dragging:
                    pyautogui.mouseUp()
                    is_dragging = False

            if abs(vx) > 0 or abs(vy) > 0:
                pyautogui.moveRel(int(vx), int(vy))
 
    img = draw_vietnamese_text(img, status_text, (10, 50), color)
    cv2.imshow("Turbo Mouse Control", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()