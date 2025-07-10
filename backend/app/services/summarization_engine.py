# services/summarization_engine.py

import os
from pathlib import Path
from typing import List, Dict
from openai import OpenAI

class SummarizationEngine:
    """Uses OpenAI v1 client to generate summaries for code files."""
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key)

    def summarize_repo(self, repo_path: str) -> List[Dict[str, str]]:
        summaries: List[Dict[str, str]] = []
        for root, _, files in os.walk(repo_path):
            for fname in files:
                if not fname.endswith(('.py', '.js', '.ts', '.java', '.go')):
                    continue
                fpath = Path(root) / fname
                content = fpath.read_text(errors='ignore')[:1500]

                prompt = f"""Summarize the purpose of this code:
                {content}
                """

                resp = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user", "content": prompt}],
                    temperature=0.2,
                )

                summary = resp.choices[0].message.content.strip()
                summaries.append({
                    "file": str(fpath.relative_to(repo_path)),
                    "summary": summary,
                })

        return summaries
