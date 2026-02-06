from fastapi import APIRouter

router = APIRouter()

@router.post("/signup")
def signup():
    return {"message": "User signup successfull"}




@router.post("/login")
def login():
    return {"message": "User login successfull"}
