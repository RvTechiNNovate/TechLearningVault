from fastapi import FastAPI, HTTPException, Depends, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import openai
import httpx
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  # Replace with a secure random key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

# OAuth2PasswordBearer for handling token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Example user database (replace with actual user management logic)
fake_users_db = {
    "user1": {
        "username": "user1",
        "hashed_password": "$argon2id$v=19$m=10240,t=10,p=8$4/G13iEOs1+1nuSfzR8FbA$yH3RxMRFI9S4K6gWZZ5h0C9e0ZuMpeYiNq1ESfnFqWw",  # Hashed password for "password1"
    }
}

# Password hashing context
pwd_context = CryptContext(schemes=["argon2"])


class ChatRequest(BaseModel):
    query: str


class Token(BaseModel):
    access_token: str
    token_type: str


def generate_jwt_token(username: str) -> str:
    """
    Generate JWT token with user information.
    """
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str):
    """
    Get user from database.
    """
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return user_dict


def authenticate_user(username: str, password: str):
    """
    Authenticate user against database.
    """
    user = get_user(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user


async def get_openai_session() -> httpx.AsyncClient:
    """
    Async context manager for HTTPX client.
    """
    async with httpx.AsyncClient() as client:
        yield client


async def retrieve_documents(query: str, client: httpx.AsyncClient) -> list:
    """
    Placeholder retrieval logic for documents.
    """
    # Replace with actual retrieval logic (e.g., database query, external API call)
    return [
        "Document 1: This is a sample document related to the query.",
        "Document 2: Another relevant document content here."
    ]


async def generate_response(query: str, client: httpx.AsyncClient) -> str:
    """
    Generate response using OpenAI API.
    """
    documents = await retrieve_documents(query, client)
    context = "\n".join(documents)

    try:
        response = await client.post(
            "https://api.openai.com/v1/engines/text-davinci-003/completions",
            headers={"Authorization": f"Bearer {openai.api_key}"},
            json={
                "prompt": f"Context: {context}\n\nQuery: {query}\n\nResponse:",
                "max_tokens": 150
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["text"].strip()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Error while requesting OpenAI API: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service unavailable")


app = FastAPI()


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint to authenticate user and provide JWT token.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return {"access_token": generate_jwt_token(user["username"]), "token_type": "bearer"}


@app.post("/chat", response_model=dict)
async def chat(request: ChatRequest, client: httpx.AsyncClient = Depends(get_openai_session), token: str = Security(oauth2_scheme)):
    """
    Endpoint to handle chat requests using OpenAI.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        response = await generate_response(request.query, client)
        return {"response": response}
    except jwt.JWTError as e:
        logger.error(f"JWT Error: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
