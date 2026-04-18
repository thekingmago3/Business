"""Publisher interface.

Every publisher takes a Piece + RenderedMedia and ships it. If credentials
are missing OR dry_run=True, it logs what it *would* do and returns a
simulated PublishResult so the pipeline is observable end-to-end without
actually posting.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..media.base import RenderedMedia
from ..storage import Piece


@dataclass
class PublishResult:
    external_id: str | None
    url: str | None
    dry_run: bool
    error: str | None = None


class Publisher(ABC):
    platform: str = "base"

    @abstractmethod
    def publish(self, piece: Piece, media: RenderedMedia) -> PublishResult:
        ...
