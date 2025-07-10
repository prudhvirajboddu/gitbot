import os
from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel

from ..config import settings
from ..services.github_client import GitHubClient
from ..services.summarization_engine import SummarizationEngine
from ..services.diff_analyzer import DiffAnalyzer
from ..services.job_store import init_job, update_job
from ..utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

class AnalyzeRequest(BaseModel):
    repo_url: str

class AnalyzeResponse(BaseModel):
    job_id: str

@router.post(
    "/repo",
    response_model=AnalyzeResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def analyze_repo(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    client = GitHubClient()
    try:
        job_id, repo_path = client.clone_repo(request.repo_url)
    except Exception as e:
        logger.error(f"Failed to start analysis for {request.repo_url}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not start analysis: " + str(e)
        )

    # Initialize job in our store
    init_job(job_id)
    # Kick off the background work
    background_tasks.add_task(run_analysis, job_id, repo_path)
    return AnalyzeResponse(job_id=job_id)

async def run_analysis(job_id: str, repo_path: str):
    """Background task: summarize, diff, persist, cleanup."""
    try:
        # 1) Summarize
        engine = SummarizationEngine()
        summaries = engine.summarize_repo(repo_path)
        update_job(job_id, status="summarized", progress=0.5)

        # 2) Diff
        differ = DiffAnalyzer()
        diffs = differ.compute_diffs(repo_path)
        update_job(job_id, status="diffed", progress=0.8)

        # 3) Persist final result
        result = {"summaries": summaries, "diffs": diffs}
        update_job(job_id, status="done", progress=1.0, result=result)
        logger.info(f"Job {job_id} done")

    except Exception as exc:
        logger.error(f"Job {job_id} failed: {exc}", exc_info=True)
        update_job(job_id, status="failed", progress=1.0)
    finally:
        # 4) Cleanup disk
        GitHubClient().cleanup(job_id)
