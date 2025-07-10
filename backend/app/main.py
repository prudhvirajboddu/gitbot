from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .api import auth, analyze, chat, status
from .config import settings
from .utils.logger import get_logger

# Initialize logging
logger = get_logger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs" if settings.ENABLE_DOCS else None,
    redoc_url="/redoc" if settings.ENABLE_DOCS else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(analyze.router, prefix="/analyze", tags=["analyze"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(status.router, prefix="/status", tags=["status"])

# Health check
@app.get("/ping", summary="Liveness probe")
async def ping():
    return {"message": "pong"}
