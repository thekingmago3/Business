"""Trend miner.

Uses Claude's server-side web_search tool to pull what's trending *right now*
for the niche, then distills to a short list of:
  - rising topics (with angle)
  - trending sounds/formats (per platform where applicable)
  - high-intent keywords

The agent caches the result for ~6h in SQLite so we don't re-fetch per slot.
Falls back to evergreen frameworks if the fetch fails or turns up nothing.
"""

from __future__ import annotations

import logging
from typing import Any

from .config import Brand
from .llm import LLM
from .storage import Storage

log = logging.getLogger(__name__)

WEB_SEARCH_TOOL = {"type": "web_search_20250305", "name": "web_search", "max_uses": 5}


SYSTEM = """You are a trend analyst for short-form social content.
Your job: surface what is TRENDING RIGHT NOW in the user's niche across
TikTok, Instagram Reels, and YouTube.

Focus on:
- rising topics and angles (not evergreen stuff)
- hashtags or audio/sound formats gaining momentum this week
- specific news, launches, or debates viewers are discussing
- creator formats that are overperforming

Be concrete. Cite dates. Skip anything older than 14 days.
Respond with JSON only, matching this shape:
{
  "fetched_for": "<niche>",
  "rising_topics": [
    {"topic": "...", "angle": "...", "evidence": "<url or source>"}
  ],
  "trending_formats": [
    {"platform": "tiktok|instagram|youtube", "format": "...", "why": "..."}
  ],
  "keywords": ["..."],
  "avoid": ["topics that are played out or risky"]
}"""


def fetch_trends(llm: LLM, brand: Brand, storage: Storage, platform: str = "all") -> dict[str, Any]:
    """Get trends, with 6h SQLite cache. Fallback to empty payload on failure."""
    cached = storage.latest_trends(platform)
    if cached is not None:
        log.info("Using cached trends for %s (<6h old).", platform)
        return cached

    user = (
        f"Niche: {brand.niche}\n"
        f"Target audience: {', '.join(brand.target_audience)}\n"
        f"Topic pillars: {', '.join(brand.topic_pillars)}\n\n"
        f"Find what is trending THIS WEEK for creators in this niche. "
        f"Use web search. Return JSON."
    )
    try:
        data = llm.generate_json(
            system=SYSTEM,
            user=user,
            max_tokens=3000,
            effort="high",
        )
    except Exception as e:  # trend fetch is best-effort
        log.warning("Trend fetch failed (%s); falling back to empty payload.", e)
        data = {"fetched_for": brand.niche, "rising_topics": [], "trending_formats": [], "keywords": [], "avoid": []}

    storage.cache_trends(platform, data)
    return data


def trends_prompt_block(trends: dict[str, Any]) -> str:
    """Format trends for the volatile (non-cached) portion of a generation prompt."""
    if not trends.get("rising_topics") and not trends.get("trending_formats"):
        return "# TRENDS\n(none fetched — use evergreen frameworks)"

    lines = ["# TRENDS (use as raw material, not as the whole video)"]
    for t in trends.get("rising_topics", [])[:8]:
        lines.append(f"- TOPIC: {t.get('topic')} — ANGLE: {t.get('angle')}")
    for f in trends.get("trending_formats", [])[:6]:
        lines.append(f"- FORMAT ({f.get('platform')}): {f.get('format')} — {f.get('why')}")
    if trends.get("keywords"):
        lines.append(f"- KEYWORDS: {', '.join(trends['keywords'][:12])}")
    if trends.get("avoid"):
        lines.append(f"- AVOID: {', '.join(trends['avoid'][:6])}")
    return "\n".join(lines)
