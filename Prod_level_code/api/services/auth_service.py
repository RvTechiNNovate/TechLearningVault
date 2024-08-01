from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["argon2"])

class AuthService:
    def authenticate_user(self, username: str, password: str) -> bool:
        """
        Authenticate user against database.
        """
        # Example user database (replace with actual user management logic)
        fake_users_db = {
            "user1": {
                "username": "user1",
                "hashed_password": "$argon2id$v=19$m=10240,t=10,p=8$4/G13iEOs1+1nuSfzR8FbA$yH3RxMRFI9S4K6gWZZ5h0C9e0ZuMpeYiNq1ESfnFqWw",  # Hashed password for "password1"
            }
        }

        user = fake_users_db.get(username)
        if not user:
            return False
        if not self.verify_password(password, user["hashed_password"]):
            return False
        return True

    def generate_jwt_token(self, username: str) -> str:
        """
        Generate JWT token with user information.
        """
        try:
            payload = {
                "sub": username,
                "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            }
            return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create JWT token") from e

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify password against hashed password.
        """
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            # Handle specific exceptions like passlib's ExpectedPasswordError if needed
            return False  # Or handle as appropriate based on your application's error handling strategy
