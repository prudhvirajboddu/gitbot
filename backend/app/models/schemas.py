from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field



class AuthRequestSchema(BaseModel):
    openai_key: str = Field(..., description="User's OpenAI API key")
    github_token: str = Field(..., description="User's GitHub token")

class AuthResponseSchema(BaseModel):
    message: str = Field(..., description="Result message for auth operations")

class AnalyzeRequestSchema(BaseModel):
    repo_url: str = Field(..., description="URL of the GitHub repository to analyze")

class AnalyzeResponseSchema(BaseModel):
    job_id: str = Field(..., description="Identifier for the analysis job")

class ChatRequestSchema(BaseModel):
    job_id: str = Field(..., description="Identifier of the analysis job")
    message: str = Field(..., description="User's chat message")

class ChatResponseSchema(BaseModel):
    reply: str = Field(..., description="Assistant's reply message")

class StatusResponseSchema(BaseModel):
    job_id:   str               = Field(...)
    status:   str               = Field(...)
    progress: float             = Field(...)
    result:   Optional[Dict[str, Any]] = Field(None)