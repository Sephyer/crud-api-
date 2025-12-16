import os
from dotenv import load_dotenv
from pathlib import Path

# Explicit path to .env in project root
dotenv_path = Path(os.getcwd()) / ".env"
if not dotenv_path.exists():
    raise FileNotFoundError(f".env file not found at {dotenv_path}")

load_dotenv(dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL =", DATABASE_URL)
