from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:

    # Fallback to local sqlite for development if needed, 
    # but since the user is using Postgres, we should probably warn or raise.
    # For now, let's raise a clear error to help debugging.
    raise ValueError("DATABASE_URL is not set. Please check your .env file at: " + env_path)

# SQLAlchemy 1.4+ removed support for the 'postgres://' prefix, but many platforms still use it.
# We'll automatically fix it to 'postgresql://' if needed.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print("DATABASE_URL found:", DATABASE_URL[:20] + "...") # Mask sensitive info but confirm loading


if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
