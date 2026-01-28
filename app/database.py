from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load .env file from project root
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)  # Load environment variables from .env

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Friendly default for quick local runs (no Postgres required).
    # You can still override this with a `.env` file or environment variable.
    DATABASE_URL = "sqlite:///./test.db"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
