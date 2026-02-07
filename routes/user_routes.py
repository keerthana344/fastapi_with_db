from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from repositories.user_repo import user_repo
from schemas.user_schema import user_schema
from models import user


router = APIRouter()

@router.post("/signup")
def signup(user_data: user_schema, db: Session = Depends(get_db)):
    repo = user_repo(db)
    new_user = user(name="New User", email=user_data.email, password=user_data.password)
    repo.create_user(new_user)
    return {"message": "User signup successful"}





@router.post("/login")
def login():
    return {"message": "User login successfull"}
