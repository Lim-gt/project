import os
from sqlalchemy.orm import Session
from database.models import User
from config.config import UPLOAD_FOLDER

def create_user(db: Session, name: str, age: int, phone: str, address: str, image_file):
    """ 사용자의 얼굴 이미지를 저장하고 회원정보를 DB에 저장 """
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    image_path = os.path.join(UPLOAD_FOLDER, f"{phone}.jpg")
    with open(image_path, "wb") as buffer:
        buffer.write(image_file.file.read())

    user = User(name=name, age=age, phone=phone, address=address, face_image=image_path)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user.id

