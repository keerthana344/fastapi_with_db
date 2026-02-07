from fastapi import APIRouter , HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from db import get_db
from models import User
from repositories.user_repo import UserRepo
from schemas.user_schemas import UserSchema
from schemas.token_schemas import Token, TokenRefresh, LoginRequest
from schemas.utils.jwt_handler import create_tokens
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


@router.post("/signup")
def signup(user: UserSchema, db: Session = Depends(get_db)):
    user_repo = UserRepo(db)
    # Check if user already exists
    existing_user = user_repo.get_user(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash the password
    hashed_password = pwd_context.hash(user.password)
    db_user = User(email=user.email, password=hashed_password)
    user_repo.add_user(db_user)
    return {"message": "User signed up successfully"}

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user_repo = UserRepo(db)
    db_user = user_repo.get_user(login_data.email)
    
    if not db_user or not pwd_context.verify(login_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Generate tokens
    tokens = create_tokens(user_id=db_user.id, email=db_user.email)
    return tokens