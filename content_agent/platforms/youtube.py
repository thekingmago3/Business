"""YouTube publisher (Shorts + long-form via Data API v3).

Uses OAuth refresh-token flow. Dry-runs when creds are missing or when the
media adapter produced only a brief. Shorts are detected by format=='short'.
"""

from __future__ import annotations

import logging

from ..media.base import RenderedMedia
from ..storage import Piece
from .base import PublishResult, Publisher

log = logging.getLogger(__name__)


class YouTubePublisher(Publisher):
    platform = "youtube"

    def __init__(self, settings):
        self.client_id = settings.yt_client_id
        self.client_secret = settings.yt_client_secret
        self.refresh_token = settings.yt_refresh_token
        self.dry_run = settings.dry_run

    def _creds_ok(self) -> bool:
        return bool(self.client_id and self.client_secret and self.refresh_token)

    def publish(self, piece: Piece, media: RenderedMedia) -> PublishResult:
        if self.dry_run or not self._creds_ok() or media.video_path is None:
            log.info("[youtube dry-run] would upload %s: %r", piece.format, piece.hook[:80])
            return PublishResult(external_id=None, url=None, dry_run=True)

        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
        except ImportError as e:
            return PublishResult(external_id=None, url=None, dry_run=False,
                                 error=f"google-api-python-client not installed: {e}")

        try:
            creds = Credentials(
                token=None,
                refresh_token=self.refresh_token,
                client_id=self.client_id,
                client_secret=self.client_secret,
                token_uri="https://oauth2.googleapis.com/token",
                scopes=["https://www.googleapis.com/auth/youtube.upload"],
            )
            creds.refresh(Request())
            yt = build("youtube", "v3", credentials=creds)

            title = piece.hook if piece.format == "short" else _long_title(piece)
            if piece.format == "short" and "#shorts" not in title.lower():
                title = f"{title} #shorts"

            body = {
                "snippet": {
                    "title": title[:100],
                    "description": _description(piece),
                    "tags": [t.lstrip("#") for t in piece.hashtags][:20],
                    "categoryId": "22",
                },
                "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
            }
            media_body = MediaFileUpload(str(media.video_path), mimetype="video/mp4", resumable=True)
            req = yt.videos().insert(part="snippet,status", body=body, media_body=media_body)
            resp = None
            while resp is None:
                _, resp = req.next_chunk()
            video_id = resp["id"]
            return PublishResult(external_id=video_id,
                                 url=f"https://youtu.be/{video_id}", dry_run=False)
        except Exception as e:
            log.exception("YouTube publish failed")
            return PublishResult(external_id=None, url=None, dry_run=False, error=str(e))


def _long_title(piece: Piece) -> str:
    return piece.hook if len(piece.hook) <= 90 else piece.caption.split("\n")[0][:90]


def _description(piece: Piece) -> str:
    tags = " ".join(piece.hashtags)
    return f"{piece.caption}\n\n{piece.cta}\n\n{tags}"[:4900]
