import os
from pathlib import Path
from typing import List, Dict

import openai

class SummarizationEngine:
    """Uses OpenAI to generate summaries for code files."""
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def summarize_repo(self, repo_path: str) -> List[Dict[str, str]]:
        summaries = []
        for root, _, files in os.walk(repo_path):
            for fname in files:
                if not fname.endswith(('.py', '.js', '.ts', '.java', '.go')):
                    continue
                fpath = Path(root) / fname
                content = fpath.read_text(errors='ignore')[:1500]
                prompt = f"Summarize the purpose of this code:\n```
{content}
```"
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user", "content": prompt}],
                    temperature=0.2,
                )
                summary = response.choices[0].message.content.strip()
                summaries.append({"file": str(fpath.relative_to(repo_path)), "summary": summary})
        return summaries
