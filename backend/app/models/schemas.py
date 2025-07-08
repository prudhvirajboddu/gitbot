from pydantic import BaseModel, Field
from typing import List, Optional

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
    job_id: str = Field(..., description="Identifier of the analysis job")
    status: str = Field(..., description="Current status of the job")
    progress: float = Field(..., description="Progress percentage of the job (0.0-1.0)")