import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/busbee")
JWT_SECRET = os.getenv("JWT_SECRET", "change_me")
TRANSLATION_API_KEY = os.getenv("TRANSLATION_API_KEY", "")
PDF_STORAGE_PATH = os.getenv("PDF_STORAGE_PATH", os.path.join(os.getcwd(), "backend", "uploads", "invoices"))
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "60"))

JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
