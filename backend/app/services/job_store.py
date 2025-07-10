# Simple in-memory store for demo purposes
from typing import Dict, Any

_jobs: Dict[str, Dict[str, Any]] = {}

def init_job(job_id: str):
    _jobs[job_id] = {"status": "pending", "progress": 0.0, "result": None}

def update_job(job_id: str, status: str, progress: float = None, result: Any = None):
    job = _jobs.get(job_id)
    if not job:
        return
    job["status"] = status
    if progress is not None:
        job["progress"] = progress
    if result is not None:
        job["result"] = result

def get_job(job_id: str):
    return _jobs.get(job_id)
