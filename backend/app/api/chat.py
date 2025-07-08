from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..services.conversation_manager import ConversationManager

router = APIRouter()

class ChatRequest(BaseModel):
    job_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Handle conversational messages post-analysis."""
    manager = ConversationManager()
    try:
        response = manager.handle_message(request.job_id, request.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return ChatResponse(reply=response)
