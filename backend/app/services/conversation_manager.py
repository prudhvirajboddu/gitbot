import os
from typing import Dict, List
import openai

from .summarization_engine import SummarizationEngine
from .diff_analyzer import DiffAnalyzer

class ConversationManager:
    """Manages conversational context for code analysis."""
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.conversations: Dict[str, List[Dict[str, str]]] = {}
        self.summaries_cache: Dict[str, List[Dict[str, str]]] = {}
        self.diffs_cache: Dict[str, List[Dict[str, str]]] = {}

    def _ensure_job(self, job_id: str):
        if job_id not in self.summaries_cache or job_id not in self.diffs_cache:
            engine = SummarizationEngine()
            diff = DiffAnalyzer()
            repo_path = f"./repos/{job_id}"
            self.summaries_cache[job_id] = engine.summarize_repo(repo_path)
            self.diffs_cache[job_id] = diff.compute_diffs(repo_path)
        if job_id not in self.conversations:
            self.conversations[job_id] = []

    def handle_message(self, job_id: str, message: str) -> str:
        self._ensure_job(job_id)
        history = self.conversations[job_id]
        context = []
        context.append({"role": "system", "content":
            "You are a helpful assistant that answers questions about the provided code repository."}
        )
        summary_texts = [f"File: {s['file']} - {s['summary']}" for s in self.summaries_cache[job_id]]
        context.append({"role": "system", "content": "\n".join(summary_texts)})
        for turn in history:
            context.append({"role": turn['role'], "content": turn['content']})
        context.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=context,
            temperature=0.2
        )
        reply = response.choices[0].message.content.strip()

        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": reply})

        return reply
