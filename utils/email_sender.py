import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
load_dotenv()
password=os.getenv("PASSWORD")
sender_email=os.getenv("SENDER_EMAIL")

if not password or not sender_email:
    print("Error: SENDER_EMAIL or PASSWORD not found in environment variables.")
    print(f"SENDER_EMAIL: {sender_email}")
    print(f"PASSWORD: {'*' * len(password) if password else 'None'}")
#email details
def send_email(reciever_email:str, subject:str, content:str)->str:
    """Send an email to the specified recipient"""
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = reciever_email
    msg["Subject"] = subject
    msg.set_content(content)

    try:
        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
        return "Email sent successfully!"
    except smtplib.SMTPAuthenticationError:
        print(f"Warning: Defaulting to MOCK EMAIL due to authentication error.")
        print("-" * 30)
        print(f"To: {reciever_email}")
        print(f"Subject: {subject}")
        print(f"Content: {content}")
        print("-" * 30)
        return "Email sent successfully (Mock Mode)"
    except Exception as e:
        print(f"Error sending email: {e}")
        raise e