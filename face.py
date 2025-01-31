import cv2
import face_recognition
import os
import csv
from datetime import datetime, timedelta

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

output_dir = "detected_faces"
log_file = "visitor_log.csv"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if not os.path.exists(log_file):
    with open(log_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Name"])

known_faces_dir = "known_faces"
known_face_encodings = []
known_face_names = []

for filename in os.listdir(known_faces_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        name = os.path.splitext(filename)[0]
        file_path = os.path.join(known_faces_dir, filename)

        image = face_recognition.load_image_file(file_path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(name)

last_seen = {}

visit_cooldown = timedelta(seconds=10)

cap = cv2.VideoCapture(0)

print("얼굴 인식 프로그램이 시작되었습니다. 'q'를 눌러 종료하세요.")

def log_visitor(name, timestamp):
    """ 방문자 정보를 visitor_log.csv 파일에 저장 """
    with open(log_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, name])

while True:
    ret, frame = cap.read()
    if not ret:
        print("카메라에서 영상을 가져올 수 없습니다.")
        break

    current_time = datetime.now()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face_frame = frame[y:y+h, x:x+w]

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_frame, [(y, x + w, y + h, x)])

        name = "Unknown"

        if face_encodings:
            face_encoding = face_encodings[0]
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            if True in matches:
                match_index = matches.index(True)
                name = known_face_names[match_index]

        if name in last_seen and (current_time - last_seen[name]) < visit_cooldown:
            continue

        last_seen[name] = current_time

        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        file_name = f"{output_dir}/{name}_{timestamp.replace(':', '-')}.jpg"
        cv2.imwrite(file_name, face_frame)

        print(f"{timestamp} - {name} 방문 기록 저장!")

        log_visitor(name, timestamp)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

