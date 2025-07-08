from pydantic import BaseSettings, Field, AnyHttpUrl
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = Field("GitHub Repo Chatbot", env="PROJECT_NAME")
    VERSION: str = Field("0.1.0", env="VERSION")

    # API Keys
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    GITHUB_TOKEN: str = Field(..., env="GITHUB_TOKEN")

    # CORS configuration
    CORS_ORIGINS: List[AnyHttpUrl] = Field(
        default=["*"],
        env="CORS_ORIGINS"
    )

    # Documentation
    ENABLE_DOCS: bool = Field(True, env="ENABLE_DOCS")

    # Logging
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        case_sensitive = True


# Instantiate settings for import
settings = Settings()
