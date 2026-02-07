from models import user
from sqlalchemy.orm import Session

class user_repo:
    def __init__(self,db:Session):
        self.db = db
    def create_user(self, user_obj: user):
        self.db.add(user_obj)
        self.db.commit()
        return user_obj
