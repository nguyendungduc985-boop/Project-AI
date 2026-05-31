# 🧠 ADVANCED COMPUTER VISION & HUMAN-COMPUTER INTERACTION (HCI) PROJECTS

<p align="center">
  <a href="#-english">English</a> • 
  <a href="#-tiếng-việt">Tiếng Việt</a> • 
  <a href="#-한국어">한국어</a>
</p>

---

## 🇺🇸 ENGLISH

A comprehensive portfolio of Artificial Intelligence and Computer Vision projects focusing on **Human-Computer Interaction (HCI)**. By leveraging state-of-the-art frameworks like **MediaPipe**, **OpenCV**, **Pygame**, and **Ursina Engine**, these applications turn standard webcam feeds into intelligent controller systems, interactive 3D simulations, and gesture-driven multimedia tools.

### 📂 Repository Components & File Analytics

* **`main.py` (Meme Gesture Recognition System):** Uses `MediaPipe Holistic` to track hand landmarks and overlays specific transparent transparent meme images onto the camera feed based on detected posture (e.g., *HELLO*, *LIKE*, or dual-hand *PEAK*).
* **`tiktok.py` (Gesture-Driven Media Controller):** A smart hands-free controller for video scrolling. It calculates the vertical threshold distance between the index finger tip and MCP joint to simulate keyboard strokes (`Up`/`Down`) for shifting videos, and measures the distance to the thumb for quick pausing (`Space`).
* **`thanhtabs.py` (Virtual Trackpad & Gesture Mouse):** Maps the user's wrist coordinates relative to a central camera "Dead Zone" to handle multi-directional mouse cursor movement with integrated velocity scaling. Simulates drag-and-drop operations (`pyautogui.mouseDown/Up`) by detecting hand-clenching behaviors ($<2$ fingers).
* **`gift.py` (Interactive Particle Simulator):** Merges `MediaPipe Hands` with a fullscreen `Pygame` canvas. The particle engine tracks fingers to generate complex visual effects based on gestures: clusters particles at the hand center, triggers a "sword rain" effect upon detecting a *Rock* sign, and spawns explosion dynamics upon open palms.
* **`ironman.py` (J.A.R.V.I.S Kernel V12 - 3D Object Grabber):** An immersive 3D assembly simulation powered by the `Ursina Engine`. Users control a 3D interface with their hand via a webcam feed. Pinching the thumb and index finger triggers a grabbing algorithm to pick up, move, and snap electronic parts (e.g., gears) in a 3D environment using LERP smoothing.
* **`index.html` (3D Web Galaxy Space):** A web-based front-end application built with `Three.js` and MediaPipe JavaScript APIs. It generates a dynamic 3D cosmic particle system that responds instantly to physical hand gestures via a browser webcam.
* **`demo.py` (Random Forest Classifier Platform):** A baseline core machine learning script using `scikit-learn` to fit a `RandomForestClassifier`. Evaluates datasets with Out-of-Bag (OOB) scoring metrics alongside real test classification accuracy.

### 🛠️ Core Technology Stack
* **AI & Vision:** MediaPipe (Hands, Holistic), OpenCV (Python & JS).
* **Automation:** PyAutoGUI (OS-level mouse/keyboard simulation).
* **Graphics & UI:** Ursina Engine (3D), Three.js (Web 3D), Pygame (2D Engine), Pillow.
* **Machine Learning:** Scikit-Learn.

---

## 🇻🇳 TIẾNG VIỆT

Kho lưu trữ tổng hợp các dự án Trí tuệ Nhân tạo và Thị giác Máy tính chuyên sâu về **Tương tác Người - Máy (HCI)**. Bằng cách khai thác sức mạnh của các framework như **MediaPipe**, **OpenCV**, **Pygame**, và **Ursina Engine**, hệ thống biến dữ liệu camera thông thường thành các bộ điều khiển thông minh, mô phỏng không gian 3D tương tác và công cụ đa phương tiện vận hành bằng cử chỉ.

### 📂 Phân Tích Chức Năng Các File Mã Nguồn

* **`main.py` (Hệ thống nhận diện cử chỉ chèn Meme):** Sử dụng `MediaPipe Holistic` để bắt tọa độ tay và cơ thể, tự động chèn các hình ảnh meme trong suốt tương ứng lên màn hình camera khi phát hiện các tư thế chuẩn như *HELLO*, *LIKE*, hoặc giơ cả hai tay (*PEAK*).
* **`tiktok.py` (Bộ điều khiển lướt Video bằng cử chỉ):** Bộ điều khiển không chạm thông minh hỗ trợ duyệt video ngắn. File sử dụng thuật toán tính khoảng cách trục dọc giữa đầu ngón trỏ và khớp tay để mô phỏng phím (`Up`/`Down`) nhằm chuyển đổi video, kết hợp đo khoảng cách tới ngón cái để tạm dừng (`Space`).
* **`thanhtabs.py` (Chuột ảo & Bàn di chuột thông minh):** Ánh xạ tọa độ cổ tay người dùng với một "Vùng chết - Dead Zone" trung tâm của camera để điều khiển con trỏ chuột hệ điều hành di chuyển đa hướng mượt mà theo gia tốc. Nhận diện trạng thái nắm tay ($< 2$ ngón giơ lên) để thực hiện thao tác kéo thả (`pyautogui.mouseDown/Up`).
* **`gift.py` (Hệ thống mô phỏng hạt Particle tương tác):** Kết hợp `MediaPipe Hands` và đồ họa `Pygame` toàn màn hình. Hệ thống tạo hiệu ứng hạt tàn ảnh theo dấu ngón tay: tụ hạt tại tâm bàn tay, tạo "mưa kiếm" khi làm cử chỉ *Rock* (trỏ và út giơ lên), hoặc kích nổ pháo hoa hạt khi xòe toàn bộ bàn tay.
* **`ironman.py` (Mô phỏng lắp ráp J.A.R.V.I.S Kernel V12):** Không gian mô phỏng lắp ráp linh kiện 3D thời gian thực chạy trên nền `Ursina Engine`. Người dùng điều khiển một con trỏ 3D bằng tay qua webcam, thực hiện bóp ngón trỏ và ngón cái để gắp, di chuyển và cố định (snap) các linh kiện điện tử (bánh răng) trong không gian 3D bằng thuật toán mượt nội suy LERP.
* **`index.html` (Không gian vũ trụ 3D Galaxy trên Web):** Ứng dụng Front-end chạy trực tiếp trên trình duyệt sử dụng `Three.js` và thư viện JavaScript của MediaPipe. Tạo ra một hệ thống hàng ngàn hạt thiên hà 3D chuyển động bồng bềnh và thay đổi trạng thái dòng chảy dựa trên cử chỉ tay.
* **`demo.py` (Nền tảng phân lớp Random Forest Classifier):** Script học máy nền tảng sử dụng thư viện `scikit-learn` để huấn luyện mô hình rừng ngẫu nhiên. Tính toán độ chính xác thông qua thang đo Out-of-Bag (OOB) và tập dữ liệu kiểm thử (Test Accuracy).

### 🛠️ Công Nghệ Sử Dụng
* **AI & Thị giác máy tính:** MediaPipe (Hands, Holistic), OpenCV.
* **Tự động hóa hệ thống:** PyAutoGUI.
* **Đồ họa & Giao diện:** Ursina Engine (3D), Three.js (Web 3D), Pygame (2D Graphics), Pillow.
* **Học máy:** Scikit-Learn.

---

## 🇰🇷 한국어

**인간-컴퓨터 상호작용(HCI)**에 초점을 맞춘 인공지능 및 컴퓨터 비전 종합 프로젝트 아카이브입니다. **MediaPipe**, **OpenCV**, **Pygame**, **Ursina Engine**과 같은 최첨단 프레임워크를 활용하여 일반 웹캠 피드를 지능형 컨트롤러 시스템, 대화형 3D 시뮬레이션 및 제스처 기반 멀티미디어 도구로 전환합니다.

### 📂 파일별 기능 분석 (File Analytics)

* **`main.py` (제스처 인식 밈 오버레이 시스템):** `MediaPipe Holistic`을 사용하여 손과 신체의 랜드마크를 추적하고, 감지된 포즈(*HELLO*, *LIKE*, 양손 *PEAK*)에 따라 카메라 피드 위에 특정 투명 밈 이미지를 실시간으로 오버레이합니다.
* **`tiktok.py` (제스처 기반 미디어 컨트롤러):** 숏폼 비디오 시청을 위한 스마트 핸즈프리 컨트롤러입니다. 검지 손가락 끝과 MCP 관절 사이의 수직 임계값 거리를 계산하여 비디오 이동을 위한 키보드 입력(`Up`/`Down`)을 시뮬레이션하고, 엄지손가락과의 거리를 측정하여 재생/일시정지(`Space`)를 제어합니다.
* **`thanhtabs.py` (가상 트랙패드 및 제스처 마우스):** 중앙 카메라 "데드존(Dead Zone)"을 기준으로 사용자의 손목 좌표를 매핑하여 속도 비례 가속도가 통합된 다방향 마우스 커서 이동을 처리합니다. 손을 쥐는 행동($2$개 미만의 손가락)을 감지하여 드래그 앤 드롭 작업(`pyautogui.mouseDown/Up`)을 수행합니다.
* **`gift.py` (대화형 파티클 시뮬레이터):** `MediaPipe Hands`와 전체 화면 `Pygame` 캔버스를 결합했습니다. 파티클 엔진은 손가락을 추적하여 제스처에 따라 복잡한 시각 효과를 생성합니다: 손 중앙에 파티클을 모으거나, *Rock* 제스처 감지 시 "검의 비(Sword Rain)" 효과를 트리거하고, 손을 펼치면 파티클 폭발 역학을 생성합니다.
* **`ironman.py` (J.A.R.V.I.S 커널 V12 - 3D 객체 그래버):** `Ursina Engine`으로 구동되는 몰입형 3D 조립 시뮬레이션입니다. 사용자는 웹캠을 통해 손으로 3D 인터페이스를 제어합니다. 엄지와 검지를 모으면 집기(Grab) 알고리즘이 트리거되어 LERP 평활화를 통해 3D 환경에서 전자 부품(기어 등)을 집고, 이동하고, 결합(Snap)할 수 있습니다.
* **`index.html` (웹 기반 3D 은하 공간):** `Three.js` 및 MediaPipe JavaScript API로 구축된 웹 프론트엔드 애플리케이션입니다. 브라우저 웹캠을 통해 실제 손 제스처에 즉각적으로 반응하는 동적 3D 우주 파티클 시스템을 생성합니다.
* **`demo.py` (랜덤 포레스트 분류기 플랫폼):** `scikit-learn`을 사용하여 `RandomForestClassifier`를 학습시키는 핵심 머신러닝 스크립트입니다. Out-of-Bag(OOB) 평가 지표와 실제 테스트 분류 정확도를 통해 데이터셋을 평가합니다.

### 🛠️ 핵심 기술 스택
* **AI & 컴퓨터 비전:** MediaPipe (Hands, Holistic), OpenCV (Python & JS).
* **자동화:** PyAutoGUI (OS 레벨 마우스/키보드 제어).
* **그래픽 및 UI:** Ursina Engine (3D), Three.js (Web 3D), Pygame (2D), Pillow.
* **머신러닝:** Scikit-Learn.

---

## 📬 Contact / Contacts / 연락처
* **Developer:** Nguyễn Đức Dũng (덕용)
* **Email:** nguyendungduc985@gmail.com
* **Major:** Artificial Intelligence (AI) @ East Asia University (Đại học Đông Á)
