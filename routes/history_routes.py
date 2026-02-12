from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db
from repositories.user_repo import User_Repo
from routes.user_routes import get_current_user
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/history", tags=["history"])

class ChatMessageSchema(BaseModel):
    id: int
    user_id: int
    message: str
    sender: str
    timestamp: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[ChatMessageSchema])
def get_user_history(token_payload: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetch all chat messages for the authenticated user."""
    user_repo = User_Repo(db)
    user_id = int(token_payload.get("sub"))
    history = user_repo.get_chat_history(user_id)
    return history
