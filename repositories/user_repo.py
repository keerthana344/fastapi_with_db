from models import User, ChatMessage, AuthEvent
from sqlalchemy.orm import Session


class User_Repo:
    def __init__(self, db: Session):
        self.db = db

    def add_user(self, user: User):
        self.db.add(user)
        self.db.commit()
        return user

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def add_chat_message(self, message: ChatMessage):
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_chat_history(self, user_id: int):
        return self.db.query(ChatMessage).filter(ChatMessage.user_id == user_id).order_by(ChatMessage.timestamp.asc()).all()

    def add_auth_event(self, event: AuthEvent):
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event