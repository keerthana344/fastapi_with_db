from fastapi import APIRouter, HTTPException, Depends
from utils.ai_response import get_completion
from pydantic import BaseModel, model_validator
from typing import Optional
import json
from sqlalchemy.orm import Session
from db import get_db
from models import ChatMessage
from repositories.user_repo import User_Repo
from routes.user_routes import get_current_user

class AIRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = "You are a helpful assistant."

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except Exception:
                return {"message": value}
        return value

class AIResponse(BaseModel):
    response: str

router = APIRouter()

@router.post("/ask", response_model=AIResponse)
def ask_ai(request: AIRequest, token_payload: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get response from AI model and save to history of authenticated user."""
    try:
        response = get_completion(request.message, request.system_prompt)
        
        # Extract the content from the Azure AI response object
        if hasattr(response, 'choices') and response.choices:
            ai_message = response.choices[0].message.content
        else:
            ai_message = str(response)
            
        # Get user_id from token
        user_id = int(token_payload.get("sub"))
        
        user_repo = User_Repo(db)
        
        # Save User Message
        db_user_msg = ChatMessage(user_id=user_id, message=request.message, sender="user")
        user_repo.add_chat_message(db_user_msg)
        
        # Save AI Message
        db_ai_msg = ChatMessage(user_id=user_id, message=ai_message, sender="ai")
        user_repo.add_chat_message(db_ai_msg)
            
        return AIResponse(response=ai_message)
    except Exception as e:
        print(f"AI error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
