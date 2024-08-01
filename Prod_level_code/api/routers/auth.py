# api/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from ..dependencies import get_token_header
from ..services.auth_service import AuthService
from ..models import Token
from utils.redis.cache_decorator import cache

router = APIRouter()

auth_service = AuthService()  # Dependency injection example


@router.post("/token", response_model=Token)
@cache(seconds=60)  # Cache the response for 60 seconds
async def login_for_access_token(token_data: dict = Depends(get_token_header)):
    try:
        token = auth_service.get_access_token(token_data)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token
    except Exception as e:
        # Log the exception
        print(f"An error occurred: {str(e)}")
        # Raise HTTPException with 500 status code for unhandled exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
