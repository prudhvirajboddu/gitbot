from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel

from ..config import settings
from ..services.github_client import GitHubClient
from ..services.summarization_engine import SummarizationEngine
from ..services.diff_analyzer import DiffAnalyzer
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
async def analyze_repo(
    request: AnalyzeRequest,
    background_tasks: BackgroundTasks
):
    """
    Trigger repository analysis asynchronously.
    Returns a job_id to poll for status.
    """
    client = GitHubClient()
    try:
        # create_job clones into settings.REPO_BASE_PATH/{job_id} and returns both
        job_id, repo_path = client.clone_repo(request.repo_url)
    except Exception as e:
        logger.error(f"Failed to enqueue analysis for {request.repo_url}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not start analysis: " + str(e)
        )

    # schedule the heavy work off to a background task
    background_tasks.add_task(run_analysis, job_id, repo_path)
    return AnalyzeResponse(job_id=job_id)

async def run_analysis(job_id: str, repo_path: str):
    """
    Background task to perform:
      1) Summarize code
      2) Analyze diffs
      3) Persist results
      4) Cleanup cloned repo
    """
    try:
        engine = SummarizationEngine()
        differ = DiffAnalyzer()

        # Summarize all code files in the repo
        summaries = engine.summarize_repo(repo_path)

        # Compute diffs (e.g. between last two commits)
        diffs = differ.compute_diffs(repo_path)

        # TODO: Persist the summaries and diffs under job_id
        # e.g. save_analysis_result(job_id, summaries, diffs)

        print(summaries)

        logger.info(f"Analysis for job {job_id} completed successfully.")

    except Exception as exc:
        logger.error(f"Analysis for job {job_id} failed: {exc}", exc_info=True)
        # Clean up on failure
        GitHubClient().cleanup(repo_path)
        # TODO: mark job as failed in your job store
        return

    # Clean up the cloned repo to free disk space
    GitHubClient().cleanup(repo_path)
    # TODO: mark job as done in your job store
