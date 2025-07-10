from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()  # makes Pydantic pick up your .env

class Settings(BaseSettings):
    PROJECT_NAME: str = Field("GitHub Repo Chatbot", env="PROJECT_NAME")
    VERSION: str      = Field("0.1.0",               env="VERSION")

    # API Keys (must be set in .env)
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    GITHUB_TOKEN:   str = Field(..., env="GITHUB_TOKEN")

    # origins = ["http://localhost:3000","http://127.0.0.1:8000"]
    # CORS configuration: we accept any origin by default,
    # and treat the env‐var as a comma-separated list of strings.
    # CORS_ORIGINS: List[str] = Field(default=["*"], env="CORS_ORIGINS")

    ENABLE_DOCS: bool = Field(True,  env="ENABLE_DOCS")
    LOG_LEVEL:   str  = Field("INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()
