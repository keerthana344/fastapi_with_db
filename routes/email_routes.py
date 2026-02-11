from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from utils.email_sender import send_email

import smtplib

router = APIRouter()

@router.post("/send-email")
def send_email_route(email: str, subject: str, content: str, db: Session = Depends(get_db)):
    """Send an email to the specified recipient."""
    try:
        message = send_email(email, subject, content)
        return {"message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")