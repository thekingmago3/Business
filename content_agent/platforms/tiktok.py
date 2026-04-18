"""TikTok publisher.

Uses TikTok's Content Posting API (Direct Post).
https://developers.tiktok.com/doc/content-posting-api-reference-direct-post/

Goes into dry-run mode if no access token or no rendered video (brief adapter).
"""

from __future__ import annotations

import logging

import httpx

from ..media.base import RenderedMedia
from ..storage import Piece
from .base import PublishResult, Publisher

log = logging.getLogger(__name__)

UPLOAD_INIT = "https://open.tiktokapis.com/v2/post/publish/video/init/"


class TikTokPublisher(Publisher):
    platform = "tiktok"

    def __init__(self, settings):
        self.token = settings.tiktok_access_token
        self.dry_run = settings.dry_run

    def publish(self, piece: Piece, media: RenderedMedia) -> PublishResult:
        if self.dry_run or not self.token or media.video_path is None:
            log.info("[tiktok dry-run] would post: %r", piece.hook[:80])
            return PublishResult(external_id=None, url=None, dry_run=True)

        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        size = media.video_path.stat().st_size
        chunk = min(size, 10 * 1024 * 1024)
        body = {
            "post_info": {
                "title": piece.caption[:150],
                "privacy_level": "PUBLIC_TO_EVERYONE",
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": size,
                "chunk_size": chunk,
                "total_chunk_count": max(1, (size + chunk - 1) // chunk),
            },
        }
        try:
            with httpx.Client(timeout=120) as c:
                r = c.post(UPLOAD_INIT, json=body, headers=headers)
                r.raise_for_status()
                data = r.json()["data"]
                upload_url = data["upload_url"]
                publish_id = data["publish_id"]
                with media.video_path.open("rb") as f:
                    c.put(upload_url, content=f.read(),
                          headers={"Content-Type": "video/mp4",
                                   "Content-Range": f"bytes 0-{size - 1}/{size}"}).raise_for_status()
            return PublishResult(external_id=publish_id, url=None, dry_run=False)
        except Exception as e:
            log.exception("TikTok publish failed")
            return PublishResult(external_id=None, url=None, dry_run=False, error=str(e))
