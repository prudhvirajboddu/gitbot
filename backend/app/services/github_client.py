import os
import uuid
from git import Repo
import shutil
from ..config import settings

class GitHubClient:
    def __init__(self):
        self.base = settings.REPO_BASE_PATH

    def clone_repo(self, repo_url: str) -> str:
        job_id = str(uuid.uuid4())
        dest = os.path.join(self.base, job_id)
        Repo.clone_from(repo_url, dest)
        return job_id, dest
    
    # def clone

    def cleanup(self, job_id: str):
        path = os.path.join(self.base, job_id)
        shutil.rmtree(path, ignore_errors=True)
