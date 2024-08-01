# config/settings.py

import os

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
