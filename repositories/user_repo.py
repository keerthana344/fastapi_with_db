from models import User
from sqlalchemy.orm import Session

class UserRepo:
    def __init__(self, db: Session):
        self.db = db
        
    def add_user(self, user_obj: User):
        self.db.add(user_obj)
        self.db.commit()
        return user_obj
    def get_user(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
