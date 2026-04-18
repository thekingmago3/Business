"""Media adapter interface.

Adapters turn a Piece (text + media_brief) into an artifact the publisher
can upload. The default adapter writes a structured brief a human/video
tool can act on; the HeyGen/Runway adapters actually render video.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from ..storage import Piece


@dataclass
class RenderedMedia:
    """What the adapter produced. `video_path` may be None for the brief adapter."""

    piece_id: int
    video_path: Path | None
    thumbnail_path: Path | None
    brief_path: Path
    kind: str  # "brief" | "video"


class MediaAdapter(ABC):
    name: str = "base"

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def render(self, piece: Piece) -> RenderedMedia:
        ...
