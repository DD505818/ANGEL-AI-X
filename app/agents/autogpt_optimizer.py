"""AutoGPT-powered strategy refinement helper."""
from __future__ import annotations

import os

from openai import AsyncOpenAI


class AutoGPTOptimizer:
    """Use OpenAI models to propose strategy improvements."""

    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not configured")
        self.client = AsyncOpenAI(api_key=api_key)

    async def suggest(self, prompt: str) -> str:
        """Return a suggestion for the provided prompt."""

        resp = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content or ""
