"""Runway Gen-3 adapter — cinematic b-roll / text-to-video.

Stub: falls back to the brief adapter when RUNWAY_API_KEY is missing so
the agent stays runnable out of the box. The real integration would call
`https://api.dev.runwayml.com/v1/image_to_video` or text-to-video and poll.
"""

from __future__ import annotations

import logging

from ..storage import Piece
from .base import MediaAdapter, RenderedMedia
from .brief import BriefAdapter

log = logging.getLogger(__name__)


class RunwayAdapter(MediaAdapter):
    name = "runway"

    def __init__(self, output_dir, api_key: str | None):
        super().__init__(output_dir)
        self.api_key = api_key
        self._fallback = BriefAdapter(output_dir) if not api_key else None

    def render(self, piece: Piece) -> RenderedMedia:
        if self._fallback:
            log.warning("RUNWAY_API_KEY not set — falling back to brief adapter.")
            return self._fallback.render(piece)
        # Real Runway integration: build prompt from piece.media_brief,
        # submit job, poll, download. Omitted here to keep the repo lean
        # and because costs are real — left as a clearly-marked extension.
        raise NotImplementedError("Runway integration is a stub — wire it up or set MEDIA_ADAPTER=brief.")
