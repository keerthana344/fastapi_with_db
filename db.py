from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables. In local dev, looks for .env relative to this file.
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # On Render, this means you need to add DATABASE_URL in the dashboard settings.
    print("CRITICAL ERROR: DATABASE_URL is not set in environment variables.")
    # We raise an error here to prevent SQLAlchemy from crashing with an obscure 'got None' message.
    raise ValueError("DATABASE_URL environment variable is missing.")

# SQLAlchemy 1.4+ removed support for the 'postgres://' prefix, but many platforms (like Render/Aiven) still use it.
# We'll automatically fix it to 'postgresql://' if needed.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print("DATABASE_URL found:", DATABASE_URL[:20] + "...") # Mask sensitive info but confirm loading

# Configure engine with SSL for PostgreSQL
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
