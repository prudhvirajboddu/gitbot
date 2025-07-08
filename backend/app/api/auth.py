from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..config import settings

router = APIRouter()

class AuthRequest(BaseModel):
    openai_key: str
    github_token: str

class AuthResponse(BaseModel):
    message: str

@router.post("/login", response_model=AuthResponse)
async def login(creds: AuthRequest):
    """Validate and store user API keys in-memory or secure store."""
    # For demo: simply verify presence
    if not creds.openai_key or not creds.github_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both OpenAI and GitHub tokens are required."
        )
    # TODO: securely store keys (e.g., session, database, vault)
    settings.OPENAI_API_KEY = creds.openai_key
    settings.GITHUB_TOKEN = creds.github_token
    return AuthResponse(message="API keys stored successfully.")