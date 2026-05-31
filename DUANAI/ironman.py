from ursina import *
import cv2
import mediapipe as mp
import math
import threading

# --- THIẾT LẬP CƠ BẢN ---
app = Ursina(title="J.A.R.V.I.S KERNEL V12")
window.fullscreen = True
window.color = color.black # Nền đen giúp tập trung
window.fps_counter.enabled = True # Theo dõi FPS

# --- QUẢN LÝ LINH KIỆN (DATA OPTIMIZATION) ---
class ElectronicComponent(Entity):
    def __init__(self, name, model='cube', c=color.cyan, **kwargs):
        super().__init__(
            model=model,
            color=c,
            alpha=0.7, 
            texture='white_cube',
            always_on_top=True,
            **kwargs
        )
        self.name = name
        self.target_pos = self.position
        self.is_selected = False
        self.is_snapped = False      
        self.connected_to = None     
        self.original_scale = self.scale

    # Đã sửa lỗi thụt lề: Hàm update này nằm TRONG class
    def update(self):
        # Tối ưu: Di chuyển mượt mà bằng lerp, tốc độ 30 bám sát tay
        if self.is_selected:
            self.position = lerp(self.position, self.target_pos, time.dt * 30) 
            self.rotation_y += time.dt * 100
            self.scale = lerp(self.scale, self.original_scale * 1.2, time.dt * 10)
        else:
            self.scale = lerp(self.scale, self.original_scale, time.dt * 5)

# --- HỆ THỐNG AI (CHẠY NGẦM) ---
class AIProcessor:
    def __init__(self):
        self.hands_data = []
        self.is_running = True
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def start(self):
        threading.Thread(target=self._process, daemon=True).start()

    def _process(self):
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.8)
        
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret: continue
            
            frame = cv2.flip(frame, 1)
            results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            if results.multi_hand_landmarks:
                self.hands_data = results.multi_hand_landmarks
            else:
                self.hands_data = []
        self.cap.release()

# --- GIAO DIỆN IRON MAN (HUD) ---
class JARVIS_HUD(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.status = Text(text="J.A.R.V.I.S: ONLINE", color=color.cyan, scale=1.5, position=(-0.8, 0.45))
        self.line = Entity(parent=self, model='quad', scale=(0.4, 0.005), position=(-0.6, 0.42), color=color.cyan)

# --- KHỞI TẠO HỆ THỐNG ---
hud = JARVIS_HUD()
ai = AIProcessor()
ai.start()
components = []
cursor = Entity(model='sphere', color=color.white, scale=0.2, always_on_top=True)

def spawn_part(part_type):
    p = ElectronicComponent(name=part_type, scale=1)
    if part_type == 'gear': p.model = 'cylinder'; p.color = color.orange
    components.append(p)

# Tạo menu chọn đồ
Button(text="Thêm Mạch", scale=(0.2, 0.05), position=(-0.7, 0.2), on_click=lambda: spawn_part('chip'))
Button(text="Thêm Bánh Răng", scale=(0.2, 0.05), position=(-0.7, 0.1), on_click=lambda: spawn_part('gear'))

# --- VÒNG LẶP CHÍNH ---
def update():
    if ai.hands_data:
        hand = ai.hands_data[0]
        idx = hand.landmark[8]
        thumb = hand.landmark[4]
        
        # Lấy tọa độ thô
        raw_pos = Vec3((idx.x - 0.5) * 16, -(idx.y - 0.5) * 10, 0)
        
        # Bám mượt trực tiếp, KHÔNG dùng smooth_pos nữa
        cursor.position = lerp(cursor.position, raw_pos, time.dt * 25)
        
        # Khoảng cách ngón tay
        dist = math.sqrt((idx.x - thumb.x)**2 + (idx.y - thumb.y)**2)
        
        if dist < 0.05: # ĐANG BÓP TAY (GRAB)
            cursor.color = color.red
            
            closest_comp = None
            min_dist = 2.0
            
            # Tìm linh kiện gần nhất
            for c in components:
                c.is_selected = False
                d = distance(cursor.position, c.position)
                if d < min_dist:
                    min_dist = d
                    closest_comp = c
            
            # Cầm vật gần nhất lên
            if closest_comp:
                closest_comp.is_selected = True
                closest_comp.target_pos = cursor.position
                
        else: # THẢ TAY RA
            cursor.color = color.white
            for c in components: 
                c.is_selected = False

def input(key):
    if key == 'escape': application.quit()

app.run()