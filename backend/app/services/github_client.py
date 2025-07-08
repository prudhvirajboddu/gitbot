import os
import shutil
import uuid
import subprocess
from pathlib import Path
from typing import Optional, Dict

from ..config import settings

class JobInfo:
    def __init__(self, job_id: str, status: str = "pending", progress: float = 0.0):
        self.job_id = job_id
        self.status = status
        self.progress = progress

class GitHubClient:
    """Handles cloning repos, tracking jobs, and job status."""
    def __init__(self, token: Optional[str] = None):
        # Use provided token or fallback to settings
        self.token = token or settings.GITHUB_TOKEN
        self.base_dir = Path("./repos")
        self.base_dir.mkdir(exist_ok=True)
        # In-memory job store (replace with DB in prod)
        self.jobs: Dict[str, JobInfo] = {}

    def create_job(self, repo_url: str) -> str:
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = JobInfo(job_id)
        # Start clone immediately (could defer)
        self.jobs[job_id].status = "cloning"
        return job_id

    def checkout(self, job_id: str) -> str:
        info = self.jobs.get(job_id)
        if not info:
            raise ValueError("Job not found")
        repo_path = self.base_dir / job_id
        # Clone into job-specific folder
        clone_url = repo_url.replace("https://", f"https://{self.token}@")
        subprocess.run(["git", "clone", clone_url, str(repo_path)], check=True)
        info.status = "cloned"
        info.progress = 0.3
        return str(repo_path)

    def get_job_status(self, job_id: str) -> Optional[JobInfo]:
        return self.jobs.get(job_id)

    def cleanup(self, job_id: str) -> None:
        folder = self.base_dir / job_id
        if folder.exists():
            shutil.rmtree(folder)
        self.jobs.pop(job_id, None)