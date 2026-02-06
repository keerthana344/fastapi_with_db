from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Database_url = "sqlite:///./test.db"
def get_db():
    db = create_engine(Database_url)
    try:
        yield db
    finally:
        db.close()