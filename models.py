from db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    sender = Column(String)  # 'user' or 'ai'
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class AuthEvent(Base):
    __tablename__ = "auth_events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_type = Column(String)  # 'login' or 'logout'
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    