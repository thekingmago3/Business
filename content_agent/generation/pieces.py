"""Generate one complete piece of content for a slot.

This is the hot path: scheduler fires → agent calls generate_piece →
media adapter renders → publisher ships. A piece here means the fully
written script + caption + hashtags + media brief, ready to hand to a
video generator.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from ..config import Brand, Schedule, SlotSpec
from ..llm import LLM
from ..storage import Piece, Storage
from .prompts import build_system_prompt, build_user_prompt

log = logging.getLogger(__name__)


def generate_piece(
    llm: LLM,
    storage: Storage,
    brand: Brand,
    schedule: Schedule,
    platform: str,
    slot: SlotSpec,
    trends_block: str,
) -> Piece:
    system = build_system_prompt(brand, storage.top_performers(platform))
    user = build_user_prompt(
        platform=platform,
        slot=slot,
        trends_block=trends_block,
        recent_hooks=storage.recent_hooks(platform),
        hook_variants=schedule.hook_variants_per_piece,
    )

    effort = "xhigh" if slot.format == "long" else "high"
    max_tokens = 8000 if slot.format == "long" else 4000

    data = llm.generate_json(system=system, user=user, max_tokens=max_tokens, effort=effort)
    _validate(data)

    piece = Piece(
        id=None,
        created_at=time.time(),
        platform=platform,
        slot_time=slot.time,
        theme=slot.theme,
        length_sec=slot.length_sec,
        format=slot.format,
        hook=data["hook"],
        framework=data.get("framework", ""),
        script=data["script"],
        caption=data.get("caption", ""),
        hashtags=list(data.get("hashtags", [])),
        cta=data.get("cta", ""),
        trend_tags=list(data.get("trend_tags", [])),
        media_brief=dict(data.get("media_brief", {})),
    )
    piece.id = storage.save_piece(piece)
    log.info("Generated piece #%s for %s@%s: %r", piece.id, platform, slot.time, piece.hook[:80])
    return piece


def _validate(data: dict[str, Any]) -> None:
    required = ("hook", "script")
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"Generated piece missing required fields: {missing}")
    if not isinstance(data["script"], dict) or "beats" not in data["script"]:
        raise ValueError("script must be an object with a 'beats' array")
