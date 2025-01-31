from fastapi import APIRouter, Form, File, UploadFile, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.db import get_db
from services.user_service import create_user

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    age: int
    phone: str
    address: str

@router.post("/register/")
async def register_user(
    name: str = Form(...),
    age: int = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user_id = create_user(db, name, age, phone, address, file)
    return JSONResponse(content={"user_id": user_id, "message": "회원가입 성공"}, ensure_ascii=False)


