"""Top-level agent orchestrator.

One call-path: for a given (platform, slot) →
  1. get trends (cached 6h)
  2. generate piece (Claude + prompt cache + analytics feedback)
  3. render via selected media adapter
  4. publish via platform publisher (dry-run if creds missing)
  5. persist post + return result
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from .config import Settings, SlotSpec
from .generation import generate_piece
from .llm import LLM
from .media import get_adapter
from .platforms import get_publisher
from .storage import Storage
from .trends import fetch_trends, trends_prompt_block

log = logging.getLogger(__name__)


@dataclass
class RunResult:
    piece_id: int
    platform: str
    slot_time: str
    external_id: str | None
    url: str | None
    dry_run: bool
    error: str | None


class ContentAgent:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm = LLM(settings.anthropic_api_key)
        self.storage = Storage(settings.db_path)
        self.media = get_adapter(
            settings.media_adapter,
            settings.output_dir,
            {"heygen": settings.heygen_api_key, "runway": settings.runway_api_key},
        )

    def run_slot(self, platform: str, slot: SlotSpec) -> RunResult:
        log.info("▶ %s @ %s — %s (%ss)", platform, slot.time, slot.theme, slot.length_sec)

        trends = fetch_trends(self.llm, self.settings.brand, self.storage, platform) \
            if self.settings.schedule.use_live_trends else {}
        trends_block = trends_prompt_block(trends)

        piece = generate_piece(
            self.llm, self.storage, self.settings.brand, self.settings.schedule,
            platform, slot, trends_block,
        )

        media = self.media.render(piece)
        publisher = get_publisher(platform, self.settings)
        result = publisher.publish(piece, media)

        assert piece.id is not None
        self.storage.record_post(
            piece_id=piece.id,
            platform=platform,
            external_id=result.external_id,
            url=result.url,
            dry_run=result.dry_run,
            error=result.error,
        )
        return RunResult(
            piece_id=piece.id, platform=platform, slot_time=slot.time,
            external_id=result.external_id, url=result.url,
            dry_run=result.dry_run, error=result.error,
        )

    def run_day(self) -> list[RunResult]:
        """Generate and publish every slot for today in one go (useful for catch-up)."""
        results = []
        for platform in ("tiktok", "instagram", "youtube"):
            for slot in self.settings.schedule.slots_for(platform):
                try:
                    results.append(self.run_slot(platform, slot))
                except Exception as e:
                    log.exception("slot %s@%s failed: %s", platform, slot.time, e)
        return results
