from fastapi import APIRouter
from db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from schemas.user_schema import user_schema


router = APIRouter()

@router.post("/signup")
def signup(db:Session = Depends(get_db)):
    user_repo=user_repo(db)
    user_repo.add_user()
    return {"message": "User signup successfull"}




@router.post("/login")
def login():
    return {"message": "User login successfull"}
