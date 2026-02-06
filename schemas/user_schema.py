from pydantic import BaseModel

class user_schema(BaseModel):
    email: str
    password: str
