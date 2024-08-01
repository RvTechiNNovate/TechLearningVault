# api/routers/chat.py

from fastapi import APIRouter, Depends, HTTPException, status
from api.models import ChatRequest
from api.dependencies import oauth2_scheme, get_openai_client, get_current_user
from api.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

@router.post("/chat", response_model=dict)
async def chat(request: ChatRequest, current_user: str = Depends(get_current_user), client = Depends(get_openai_client)):
    """
    Endpoint to handle chat requests using OpenAI.
    """
    try:
        response = await ai_service.generate_response(request.query, client)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
