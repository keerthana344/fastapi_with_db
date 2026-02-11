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
        send_email(email, subject, content)
        return {"message": "Email sent successfully"}
    except smtplib.SMTPAuthenticationError:
        raise HTTPException(
            status_code=500, 
            detail="Authentication failed. Please check SENDER_EMAIL and PASSWORD in your .env file."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")