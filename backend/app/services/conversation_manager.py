# services/conversation_manager.py

import os
from typing import Dict, List
from openai import OpenAI

from .summarization_engine import SummarizationEngine
from .diff_analyzer import DiffAnalyzer

class ConversationManager:
    """Manages conversational context for code analysis using OpenAI v1 client."""
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key)

        self.conversations: Dict[str, List[Dict[str, str]]] = {}
        self.summaries_cache: Dict[str, List[Dict[str, str]]] = {}
        self.diffs_cache: Dict[str, List[Dict[str, str]]] = {}

    def _ensure_job(self, job_id: str):
        if job_id not in self.summaries_cache or job_id not in self.diffs_cache:
            repo_path = os.path.join("repos", job_id)
            self.summaries_cache[job_id] = SummarizationEngine().summarize_repo(repo_path)
            self.diffs_cache[job_id]     = DiffAnalyzer().compute_diffs(repo_path)
        if job_id not in self.conversations:
            self.conversations[job_id] = []

    def handle_message(self, job_id: str, message: str) -> str:
        self._ensure_job(job_id)

        # Build the chat context
        history = self.conversations[job_id]
        system_prompt = [
            {"role":"system", "content":
                "You are a helpful assistant that answers questions "
                "about the provided code repository."}
        ]
        summary_content = "\n".join(
            f"File: {s['file']} — {s['summary']}"
            for s in self.summaries_cache[job_id]
        )
        system_prompt.append({"role":"system", "content": summary_content})

        # interleave history and the new user message
        messages = system_prompt + history + [{"role":"user", "content": message}]

        # call the new client interface
        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.2,
        )
        reply = resp.choices[0].message.content.strip()

        # update history
        history.append({"role":"user", "content": message})
        history.append({"role":"assistant", "content": reply})

        return reply
