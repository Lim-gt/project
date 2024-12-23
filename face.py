import cv2
import sqlite3
from datetime import datetime

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

conn = sqlite3.connect('gyeongtaekdb.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS FaceDetection (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    x INTEGER,
    y INTEGER,
    width INTEGER,
    height INTEGER
)
''')
conn.commit()

cap = cv2.VideoCapture(0)

print("얼굴 인식 프로그램이 시작되었습니다. 'q'를 눌러 종료하세요.")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("카메라에서 영상을 가져올 수 없습니다.")
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
        INSERT INTO FaceDetection (timestamp, x, y, width, height)
        VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, x, y, w, h))
        conn.commit()
    
    cv2.imshow('Face Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
conn.close()
