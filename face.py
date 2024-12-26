import cv2
import os
from datetime import datetime

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

output_dir = "detected_faces"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

last_face_position = None
last_detected_time = None
capture_delay = 2
tolerance = 300 

cap = cv2.VideoCapture(0)

print("얼굴 인식 프로그램이 시작되었습니다. 'q'를 눌러 종료하세요.")

def is_position_similar(pos1, pos2, tolerance):
    if pos1 is None or pos2 is None:
        return False
    x1, y1, w1, h1 = pos1
    x2, y2, w2, h2 = pos2
    return (
        abs(x1 - x2) <= tolerance and
        abs(y1 - y2) <= tolerance and
        abs(w1 - w2) <= tolerance and
        abs(h1 - h2) <= tolerance
    )

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("카메라에서 영상을 가져올 수 없습니다.")
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    current_time = datetime.now()
    
    if len(faces) > 0:
        x, y, w, h = faces[0]
        current_face_position = (x, y, w, h)
        
        if last_face_position and is_position_similar(last_face_position, current_face_position, tolerance):
            if last_detected_time and (current_time - last_detected_time).total_seconds() >= capture_delay:
                face_img = frame[y:y+h, x:x+w]
                timestamp = current_time.strftime('%Y%m%d_%H%M%S_%f')
                file_name = f"{output_dir}/face_{timestamp}.jpg"
                cv2.imwrite(file_name, face_img)
                print(f"얼굴이 저장되었습니다: {file_name}")
                last_detected_time = None
        else:
            last_detected_time = current_time
            last_face_position = current_face_position
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    else:
        last_face_position = None
        last_detected_time = None
    
    cv2.imshow('Face Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

