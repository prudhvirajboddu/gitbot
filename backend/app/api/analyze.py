from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from ..services.github_client import GitHubClient
from ..services.summarization_engine import SummarizationEngine
from ..services.diff_analyzer import DiffAnalyzer

router = APIRouter()

class AnalyzeRequest(BaseModel):
    repo_url: str

class AnalyzeResponse(BaseModel):
    job_id: str

@router.post("/repo", response_model=AnalyzeResponse)
async def analyze_repo(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    """Trigger repository analysis asynchronously."""
    client = GitHubClient(token=None)
    try:
        job_id = client.create_job(request.repo_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    background_tasks.add_task(run_analysis, job_id)
    return AnalyzeResponse(job_id=job_id)

async def run_analysis(job_id: str):
    """Background task to perform clone, summarize, diff."""
    engine = SummarizationEngine()
    diff = DiffAnalyzer()
    # 1. Clone and parse
    repo_path = GitHubClient().checkout(job_id)
    # 2. Summarize code
    summaries = engine.summarize_repo(repo_path)
    # 3. Analyze diffs
    diffs = diff.compute_diffs(repo_path)
    # TODO: persist results
