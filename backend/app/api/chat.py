import os
from fastapi import APIRouter, HTTPException, status
from ..config import settings
from ..services.conversation_manager import ConversationManager
from ..models.schemas import ChatRequestSchema, ChatResponseSchema

router = APIRouter()
conv = ConversationManager()

@router.post(
    "/chat",
    response_model=ChatResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def chat_endpoint(req: ChatRequestSchema):
    job_id = req.job_id
    repo_path = os.path.join(settings.REPO_BASE_PATH, job_id)

    if not os.path.isdir(repo_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Repo directory for job {job_id!r} not found"
        )

    try:
        reply = conv.handle_message(job_id, req.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    # Return as a Pydantic model (FastAPI will JSON-serialize it)
    return ChatResponseSchema(reply=reply)
