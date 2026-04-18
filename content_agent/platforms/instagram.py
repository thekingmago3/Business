"""Instagram publisher (Reels via Graph API).

https://developers.facebook.com/docs/instagram-platform/content-publishing

Reels require a publicly-reachable video URL for the container step; we
upload to wherever you host first (S3/CDN) — this stub assumes you'll
provide a URL-producing step. In dry-run / no-creds mode it just logs.
"""

from __future__ import annotations

import logging
import time

import httpx

from ..media.base import RenderedMedia
from ..storage import Piece
from .base import PublishResult, Publisher

log = logging.getLogger(__name__)

GRAPH = "https://graph.facebook.com/v20.0"


class InstagramPublisher(Publisher):
    platform = "instagram"

    def __init__(self, settings):
        self.token = settings.ig_access_token
        self.ig_user_id = settings.ig_user_id
        self.dry_run = settings.dry_run

    def publish(self, piece: Piece, media: RenderedMedia) -> PublishResult:
        if self.dry_run or not self.token or not self.ig_user_id or media.video_path is None:
            log.info("[instagram dry-run] would post reel: %r", piece.hook[:80])
            return PublishResult(external_id=None, url=None, dry_run=True)

        # A real deploy hosts the file and passes a public URL here.
        video_url = getattr(media, "public_url", None)
        if not video_url:
            return PublishResult(external_id=None, url=None, dry_run=True,
                                 error="No public video URL available for IG container step.")

        try:
            with httpx.Client(timeout=120) as c:
                create = c.post(
                    f"{GRAPH}/{self.ig_user_id}/media",
                    params={
                        "media_type": "REELS",
                        "video_url": video_url,
                        "caption": _caption(piece),
                        "access_token": self.token,
                    },
                )
                create.raise_for_status()
                creation_id = create.json()["id"]

                for _ in range(30):
                    s = c.get(f"{GRAPH}/{creation_id}",
                              params={"fields": "status_code", "access_token": self.token}).json()
                    if s.get("status_code") == "FINISHED":
                        break
                    if s.get("status_code") in ("ERROR", "EXPIRED"):
                        raise RuntimeError(f"IG container error: {s}")
                    time.sleep(5)

                pub = c.post(
                    f"{GRAPH}/{self.ig_user_id}/media_publish",
                    params={"creation_id": creation_id, "access_token": self.token},
                )
                pub.raise_for_status()
                media_id = pub.json()["id"]
            return PublishResult(external_id=media_id, url=None, dry_run=False)
        except Exception as e:
            log.exception("Instagram publish failed")
            return PublishResult(external_id=None, url=None, dry_run=False, error=str(e))


def _caption(piece: Piece) -> str:
    tags = " ".join(piece.hashtags)
    return f"{piece.caption}\n\n{piece.cta}\n\n{tags}"[:2200]
