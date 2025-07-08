import subprocess
import os
from pathlib import Path
from typing import List, Dict

class DiffAnalyzer:
    """Analyzes git diffs for a repo."""
    def compute_diffs(self, repo_path: str) -> List[Dict[str, str]]:
        repo_dir = Path(repo_path)
        os_cwd = os.getcwd()
        os.chdir(repo_dir)
        try:
            raw = subprocess.check_output(["git", "log", "--pretty=format:%H"], text=True)
            commit_ids = raw.splitlines()
            diffs = []
            for cid in commit_ids[:10]:
                diff_text = subprocess.check_output(["git", "show", cid, "--stat"], text=True)
                diffs.append({"commit": cid, "diff": diff_text})
            return diffs
        finally:
            os.chdir(os_cwd)