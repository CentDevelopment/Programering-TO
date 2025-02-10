import cv2
import numpy as np
import time

# Funksjon for å finne tilgjengelige kameraer
def find_available_cameras():
    available_cameras = []
    for i in range(10):  # Tester fra 0 til 9
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras

# Funksjon for å finne dartbrettet i bildet
def find_dartboard(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1.2, 100, param1=50, param2=30, minRadius=100, maxRadius=300)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        return circles[0][0]  # Returnerer første sirkelen funnet (x, y, radius)
    return None

# Funksjon for å oppdage endringer i bildet
def detect_hit(previous_frame, current_frame):
    diff = cv2.absdiff(previous_frame, current_frame)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(largest_contour)
        return (x + w // 2, y + h // 2)  # Returnerer midtpunktet av treffområdet
    return None

# Funksjon for å beregne poeng
def calculate_score(hit_point, dartboard):
    if dartboard is None:
        return 0  # Hvis dartbrettet ikke er funnet ennå
    
    x, y, radius = dartboard
    dx = hit_point[0] - x
    dy = hit_point[1] - y
    distance = np.sqrt(dx**2 + dy**2)
    
    # Enkel poengberegning basert på avstand til sentrum
    if distance < radius * 0.1:
        return 50  # Bullseye
    elif distance < radius * 0.2:
        return 25  # Ytre bullseye
    elif distance < radius * 0.4:
        return 10  # Indre ringer
    elif distance < radius * 0.6:
        return 5  # Ytre ringer
    else:
        return 0  # Utenfor poengområdet

# Finn tilgjengelige kameraer
camera_indices = find_available_cameras()
if len(camera_indices) < 3:
    print("Fant ikke nok kameraer! Minst 3 kameraer kreves.")
    exit()

# Åpne tre kameraer
cap1 = cv2.VideoCapture(camera_indices[1])
cap2 = cv2.VideoCapture(camera_indices[2])
cap3 = cv2.VideoCapture(camera_indices[3])

# Les første bilder for kalibrering
_, frame1 = cap1.read()
_, frame2 = cap2.read()
_, frame3 = cap3.read()
previous_frames = [frame1.copy(), frame2.copy(), frame3.copy()]

# Finn dartbrett
dartboard1 = find_dartboard(frame1)
dartboard2 = find_dartboard(frame2)
dartboard3 = find_dartboard(frame3)

total_score = 0

for i in range(3):  # Simulerer 3 kast
    print(f"Kast {i+1}...")
    time.sleep(2)  # Simulerer tiden mellom kast
    
    _, frame1 = cap1.read()
    _, frame2 = cap2.read()
    _, frame3 = cap3.read()
    
    hit1 = detect_hit(previous_frames[0], frame1)
    hit2 = detect_hit(previous_frames[1], frame2)
    hit3 = detect_hit(previous_frames[2], frame3)
    
    previous_frames = [frame1.copy(), frame2.copy(), frame3.copy()]
    
    score1 = calculate_score(hit1, dartboard1) if hit1 else 0
    score2 = calculate_score(hit2, dartboard2) if hit2 else 0
    score3 = calculate_score(hit3, dartboard3) if hit3 else 0
    
    total_score += max(score1, score2, score3)  # Tar den beste poengsummen fra 3 kameraer
    
    print(f"Treffpunkter: {hit1}, {hit2}, {hit3}, Poeng: {max(score1, score2, score3)}")

print(f"Total score: {total_score}")
cap1.release()
cap2.release()
cap3.release()
cv2.destroyAllWindows()
