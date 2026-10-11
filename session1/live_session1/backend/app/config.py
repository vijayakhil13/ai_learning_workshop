import os
from pathlib import Path
from dotenv import load_dotenv
BACKEND_DIR= Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / ".env")
load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY","").strip()
GROQ_MODEL=os.getenv("GROQ_MODEL","").strip()