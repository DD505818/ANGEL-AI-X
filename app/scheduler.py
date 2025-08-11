"""APScheduler jobs for warmup, housekeeping, and backtests."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import delete

from .db import get_session
from .models import RiskMetric

logger = logging.getLogger(__name__)


async def warmup() -> None:
    """Warmup job executed at startup."""
    logger.info("Warmup job executed")


async def housekeeping() -> None:
    """Remove risk metrics older than 30 days."""
    async with get_session() as session:
        cutoff = datetime.utcnow() - timedelta(days=30)
        await session.execute(delete(RiskMetric).where(RiskMetric.created_at < cutoff))
        logger.info("Housekeeping removed old risk metrics")


async def backtest() -> None:
    """Run a simple backtest placeholder."""
    logger.info("Backtest job executed")


def start_scheduler() -> AsyncIOScheduler:
    """Start background scheduler with configured jobs."""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(warmup, "date")
    scheduler.add_job(housekeeping, "cron", hour=0)
    scheduler.add_job(backtest, "cron", hour="*/6")
    scheduler.start()
    return scheduler
