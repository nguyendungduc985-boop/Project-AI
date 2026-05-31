import cv2
import mediapipe as mp
import os
import numpy as np

# --- CẤU HÌNH ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "assets")
# Điều chỉnh kích thước meme nhỏ lại một chút để phù hợp với chiều ngang 320
MEME_SIZE = (120, 120) 
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):
    try:
        bg_img = background_img.copy()
        if overlay_size is not None:
            img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

        if img_to_overlay_t.shape[2] == 3:
            img_to_overlay_t = cv2.cvtColor(img_to_overlay_t, cv2.COLOR_BGR2BGRA)

        b,g,r,a = cv2.split(img_to_overlay_t)
        overlay_color = cv2.merge((b,g,r))
        mask = cv2.medianBlur(a,5)
        
        h, w, _ = overlay_color.shape
        
        if y+h > bg_img.shape[0] or x+w > bg_img.shape[1] or y < 0 or x < 0:
            return bg_img
            
        roi = bg_img[y:y+h, x:x+w]
        img1_bg = cv2.bitwise_and(roi.copy(),roi.copy(),mask = cv2.bitwise_not(mask))
        img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)
        bg_img[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)
        return bg_img
    except:
        return background_img

# Tải ảnh meme
gesture_memes = {}
meme_files = {"LIKE": "like_meme.png", "HELLO": "hello_meme.png", "PEAK": "peak_meme.png"}

if os.path.exists(ASSETS_DIR):
    for gesture, filename in meme_files.items():
        path = os.path.join(ASSETS_DIR, filename)
        try:
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if img is not None: 
                gesture_memes[gesture] = img
        except: 
            pass
else:
    print(f"Không tìm thấy thư mục assets")

def get_finger_status(lm):
    fingers = []
    # Ngón cái (Thumb)
    if abs(lm[4].x - lm[17].x) > abs(lm[3].x - lm[17].x): fingers.append(1)
    else: fingers.append(0)
    # 4 ngón còn lại
    tips = [8, 12, 16, 20]; pips = [6, 10, 14, 18]
    for tip, pip in zip(tips, pips):
        if lm[tip].y < lm[pip].y: fingers.append(1)
        else: fingers.append(0)
    return fingers

def detect_gesture(fingers):
    if fingers == [1, 1, 1, 1, 1]: return "HELLO"
    elif fingers == [1, 0, 0, 0, 0]: return "LIKE"
    return None

# --- CHƯƠNG TRÌNH CHÍNH ---
cap = cv2.VideoCapture(0)

# Cài đặt độ phân giải 320x640
# Lưu ý: Một số webcam không hỗ trợ đúng tỷ lệ dọc, ta sẽ resize thủ công nếu cần
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

window_name = "AI Camera 320x640"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
# Nếu muốn xem đúng tỉ lệ dọc, không nên để FULLSCREEN vì nó sẽ làm giãn hình
# cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        # Ép kiểu frame về đúng 320x640 nếu webcam mặc định là 640x480
        frame = cv2.resize(frame, (320, 640))
        frame = cv2.flip(frame, 1)
        h_frame, w_frame, _ = frame.shape
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Vẽ landmarks (khung xương)
        if results.right_hand_landmarks:
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        if results.left_hand_landmarks:
            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        current_gesture_key = None
        msg = ""
        color = (200, 200, 200)

        # Logic nhận diện
        if results.right_hand_landmarks and results.left_hand_landmarks:
            current_gesture_key = "PEAK"
            msg = "PEAK!"
            color = (0, 255, 255)
        else:
            hand_landmarks = results.right_hand_landmarks or results.left_hand_landmarks
            if hand_landmarks:
                fingers_status = get_finger_status(hand_landmarks.landmark)
                gesture = detect_gesture(fingers_status)
                if gesture == "HELLO":
                    current_gesture_key = "HELLO"
                    msg = "HI!"
                    color = (0, 255, 0)
                elif gesture == "LIKE":
                    current_gesture_key = "LIKE"
                    msg = "LIKE!"
                    color = (0, 0, 255)

        # Hiển thị Meme
        if current_gesture_key and current_gesture_key in gesture_memes:
            # Đặt meme ở góc trên bên phải, cách lề 20px
            x_pos = w_frame - MEME_SIZE[0] - 20
            image = overlay_transparent(image, gesture_memes[current_gesture_key], x_pos, 20, MEME_SIZE)

        # Hiển thị Text (Chỉnh scale nhỏ lại vì màn hình hẹp)
        if msg:
            cv2.putText(image, msg, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.imshow(window_name, image)
        if cv2.waitKey(10) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()