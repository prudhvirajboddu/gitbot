from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services.github_client import GitHubClient

router = APIRouter()

class StatusResponse(BaseModel):
    job_id: str
    status: str
    progress: float

@router.get("/{job_id}", response_model=StatusResponse)
async def get_status(job_id: str):
    """Return status of background analysis job."""
    client = GitHubClient()
    info = client.get_job_status(job_id)
    if not info:
        raise HTTPException(status_code=404, detail="Job not found.")
    return StatusResponse(job_id=job_id, status=info.status, progress=info.progress)