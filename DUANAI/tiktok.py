import cv2
import mediapipe as mp
import pyautogui
import time
import math

pyautogui.FAILSAFE = False
COOLDOWN = 1.5    
THRESHOLD = 0.05  
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

last_action_time = 0 

with mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
    max_num_hands=2) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        h_frame, w_frame, _ = frame.shape
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        action_text = ""
        current_time = time.time()

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                lm = hand_landmarks.landmark

                
                index_tip_y = lm[8].y  
                index_mcp_y = lm[5].y  
                

                ix, iy = int(lm[8].x * w_frame), int(lm[8].y * h_frame)
                tx, ty = int(lm[4].x * w_frame), int(lm[4].y * h_frame)

                cv2.circle(image, (ix, iy), 10, (0, 255, 255), cv2.FILLED)


                distance = math.hypot(ix - tx, iy - ty)
                if distance < 30:
                    if current_time - last_action_time > COOLDOWN:
                        pyautogui.press('space')
                        action_text = "DUNG / PHAT"
                        last_action_time = current_time
                        cv2.circle(image, (ix, iy), 25, (0, 0, 255), cv2.FILLED)

                else:
                    if current_time - last_action_time > COOLDOWN:
                        if index_tip_y < index_mcp_y - THRESHOLD:
                            pyautogui.press('up') 
                            action_text = "LEN (PREV)"
                            last_action_time = current_time

                        elif index_tip_y > index_mcp_y + THRESHOLD:
                            pyautogui.press('down') 
                            action_text = "XUONG (NEXT)"
                            last_action_time = current_time

        if action_text:
            cv2.putText(image, action_text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        cv2.imshow('Dieu khien Tikok Bang Tay', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()