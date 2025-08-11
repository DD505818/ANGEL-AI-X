"""Asynchronous sentiment ingestion utilities."""

from __future__ import annotations

import asyncio
from typing import AsyncIterator, Dict

_POSITIVE = {"gain", "up", "profit", "bull"}
_NEGATIVE = {"loss", "down", "bear", "sell"}


async def ingest_sentiment(source: AsyncIterator[str]) -> AsyncIterator[float]:
    """Yield sentiment scores from an asynchronous text stream.

    The function reconnects on errors with exponential backoff.

    Args:
        source: Async iterator producing text snippets.

    Yields:
        Sentiment scores in [-1, 1].
    """

    backoff = 1.0
    while True:
        try:
            async for text in source:
                yield _score_text(text)
            return
        except Exception:
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 30)


def _score_text(text: str) -> float:
    words = {w.lower() for w in text.split()}
    pos = len(words & _POSITIVE)
    neg = len(words & _NEGATIVE)
    total = pos + neg
    if total == 0:
        return 0.0
    return (pos - neg) / total
