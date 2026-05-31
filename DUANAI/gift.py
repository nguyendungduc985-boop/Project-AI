import cv2
import mediapipe as mp
import pygame
import random
import math
import sys

pygame.init()
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("TikTok Clone - Pure Visual")
clock = pygame.time.Clock()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

class Particle:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.vx = 0.0
        self.vy = 0.0
        # Tone màu Xanh Lá + Vàng y hệt video
        self.color = (random.randint(150, 255), random.randint(200, 255), random.randint(0, 100))
        self.size = random.randint(2, 4)
        
        # Biến dùng cho việc tạo hình khối cầu 3D giả lập
        self.angle = random.uniform(0, math.pi * 2)
        self.radius = random.uniform(50, 250)
        self.speed = random.uniform(0.02, 0.05)

    def update(self, target_x, target_y, gesture):
        if gesture == "RAIN":
            # HIỆU ỨNG MƯA KIẾM (Rơi thẳng đứng)
            self.vy += 1.5 # Lực hút trái đất
            self.vx *= 0.5 # Triệt tiêu lực ngang
            if self.vy > 30: self.vy = 30 # Tốc độ max
            
            self.x += self.vx
            self.y += self.vy
            
            # Rớt xuống đáy thì vòng lên đỉnh
            if self.y > HEIGHT + 50:
                self.y = random.randint(-200, -50)
                self.x = random.randint(0, WIDTH)
                self.vy = random.uniform(10, 20)
                self.vx = 0

        else:
            # Các hiệu ứng xoay quanh bàn tay
            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.hypot(dx, dy)
            if dist < 1: dist = 1

            if gesture == "SPHERE":
                # TẠO KHỐI CẦU XOAY (Mô phỏng 3D)
                self.angle += self.speed
                # Cố định bán kính để tạo viền quả cầu rỗng
                target_radius = 200 + math.sin(self.angle * 3) * 50 
                self.radius += (target_radius - self.radius) * 0.1
                
                desired_x = target_x + math.cos(self.angle) * self.radius
                desired_y = target_y + math.sin(self.angle) * (self.radius * 0.5) # Nhân 0.5 để tạo độ dẹt 3D
                
                self.vx += (desired_x - self.x) * 0.1
                self.vy += (desired_y - self.y) * 0.1
                self.vx *= 0.85
                self.vy *= 0.85

            elif gesture == "EXPLODE":
                # BÙNG NỔ PHÁO HOA
                force = 2000 / dist
                self.vx -= (dx / dist) * force 
                self.vy -= (dy / dist) * force 
                self.vx *= 0.95
                self.vy *= 0.95
                
            elif gesture == "GATHER":
                # TỤ KHÍ
                pull = dist * 0.15
                self.vx += (dx / dist) * pull
                self.vy += (dy / dist) * pull
                self.vx *= 0.75
                self.vy *= 0.75

            self.x += self.vx
            self.y += self.vy

            # Ép hạt khum bay ra khỏi màn hình
            if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
                self.x = target_x + random.randint(-10, 10)
                self.y = target_y + random.randint(-10, 10)

    def draw(self, surface, gesture):
        if gesture == "RAIN":
            # Vẽ mũi kiếm dài rơi xuống
            pygame.draw.line(surface, self.color, (int(self.x), int(self.y - 40)), (int(self.x), int(self.y)), self.size + 1)
        else:
            # Vẽ vệt sáng
            pygame.draw.line(surface, self.color, (int(self.x - self.vx), int(self.y - self.vy)), (int(self.x), int(self.y)), self.size)


particles = [Particle() for _ in range(1500)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    success, img = cap.read()
    if not success: continue
    
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    gesture = "SPHERE"
    target_x, target_y = WIDTH // 2, HEIGHT // 2

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            
            # --- KIỂM TRA TỪNG NGÓN TAY ---
            tips = [8, 12, 16, 20]
            pips = [6, 10, 14, 18]
            
            is_open = []
            for tip, pip in zip(tips, pips):
                is_open.append(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y)
                
            index_up = is_open[0]
            middle_up = is_open[1]
            ring_up = is_open[2]
            pinky_up = is_open[3]
            
            fingers_count = sum(is_open)

            # --- LOGIC GESTURE Y HỆT VIDEO ---
            if fingers_count == 0:
                # Nắm tay -> Tụ khí
                gesture = "GATHER"
                target_x = int(hand_landmarks.landmark[9].x * WIDTH)
                target_y = int(hand_landmarks.landmark[9].y * HEIGHT)
                
            elif index_up and pinky_up and not middle_up and not ring_up:
                # Dấu Rock (Trỏ & Út giơ lên) -> MƯA KIẾM
                gesture = "RAIN"
                
            elif fingers_count >= 4:
                # Xòe tay -> Pháo hoa nổ
                gesture = "EXPLODE"
                target_x = int(hand_landmarks.landmark[9].x * WIDTH)
                target_y = int(hand_landmarks.landmark[9].y * HEIGHT)
                
            elif index_up and middle_up:
                # Giơ 2 ngón (Trỏ & Giữa) -> Khối cầu xoay theo tay
                gesture = "SPHERE"
                mid_x = (hand_landmarks.landmark[8].x + hand_landmarks.landmark[12].x) / 2
                mid_y = (hand_landmarks.landmark[8].y + hand_landmarks.landmark[12].y) / 2
                target_x = int(mid_x * WIDTH)
                target_y = int(mid_y * HEIGHT)
                
            else:
                gesture = "SPHERE"
                target_x = int(hand_landmarks.landmark[9].x * WIDTH)
                target_y = int(hand_landmarks.landmark[9].y * HEIGHT)

    # Hiệu ứng nền đen mờ tạo tàn ảnh
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))
    fade_surface.set_alpha(35) 
    screen.blit(fade_surface, (0, 0))

    # Cập nhật hạt
    for p in particles:
        p.update(target_x, target_y, gesture)
        p.draw(screen, gesture)

    pygame.display.flip()
    clock.tick(60)

cap.release()
pygame.quit()
sys.exit()