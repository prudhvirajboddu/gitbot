from fastapi import APIRouter, HTTPException, status
from ..models.schemas import StatusResponseSchema
from ..services.job_store import get_job

router = APIRouter()

@router.get(
    "/{job_id}",
    response_model=StatusResponseSchema,
    status_code=status.HTTP_200_OK
)
def status_endpoint(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "job_id":   job_id,
        "status":   job["status"],
        "progress": job["progress"],
        "result":   job.get("result")
    }
