"""Analytics feedback loop.

The agent learns from what actually shipped:
  1. fetch per-post metrics from each platform (stubbed where APIs require
     more setup than is reasonable in a repo skeleton)
  2. persist metrics
  3. surface top performers → piped into the generation system prompt as
     'learnings from top performers' so Claude leans into what's working

The loop is idempotent — safe to run daily.
"""

from __future__ import annotations

import logging
from typing import Any

from .config import Settings
from .storage import Storage

log = logging.getLogger(__name__)


def refresh_metrics(settings: Settings, storage: Storage) -> int:
    """Fetch analytics for all posts from the last N days and persist.

    This is a stub that mirrors real integrations: in production you'd call
    the TikTok Research API, IG Graph insights, and YouTube Analytics API.
    Returns number of posts for which metrics were refreshed.
    """
    if settings.dry_run:
        log.info("[analytics] dry-run: skipping metrics fetch.")
        return 0

    count = 0
    # Real platform API calls go here. Each platform has auth + rate limits
    # and different endpoint shapes; the DB layer is ready for the results
    # via storage.record_metrics(post_id, dict_of_metrics).
    log.info("[analytics] metrics refresh not yet wired to live APIs.")
    return count


def summarize_for_prompt(storage: Storage, platform: str) -> list[dict[str, Any]]:
    """Top-engagement pieces surfaced back into the generation prompt."""
    return storage.top_performers(platform, limit=5)
