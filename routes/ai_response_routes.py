from fastapi import APIRouter, HTTPException
from utils.ai_response import get_completion
from pydantic import BaseModel, model_validator
from typing import Optional
import json

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
def ask_ai(request: AIRequest):
    """Get response from AI model."""
    try:
        response = get_completion(request.message, request.system_prompt)
        
        # Extract the content from the Azure AI response object
        if hasattr(response, 'choices') and response.choices:
            ai_message = response.choices[0].message.content
        else:
            ai_message = str(response)
            
        return AIResponse(response=ai_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))