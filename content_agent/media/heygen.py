"""HeyGen adapter — talking-head avatar video.

Stub: submits the script to HeyGen's v2 video API, polls for completion,
downloads the MP4. Falls back to writing a brief if the API key is missing.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime

import httpx

from ..storage import Piece
from .base import MediaAdapter, RenderedMedia
from .brief import BriefAdapter

log = logging.getLogger(__name__)

HEYGEN_BASE = "https://api.heygen.com/v2"


class HeyGenAdapter(MediaAdapter):
    name = "heygen"

    def __init__(self, output_dir, api_key: str | None, avatar_id: str = "default", voice_id: str = "default"):
        super().__init__(output_dir)
        self.api_key = api_key
        self.avatar_id = avatar_id
        self.voice_id = voice_id
        self._fallback = BriefAdapter(output_dir) if not api_key else None

    def render(self, piece: Piece) -> RenderedMedia:
        if self._fallback:
            log.warning("HEYGEN_API_KEY not set — falling back to brief adapter.")
            return self._fallback.render(piece)

        script_text = " ".join(b.get("line", "") for b in piece.script.get("beats", []))
        body = {
            "video_inputs": [{
                "character": {"type": "avatar", "avatar_id": self.avatar_id, "avatar_style": "normal"},
                "voice": {"type": "text", "input_text": script_text, "voice_id": self.voice_id},
            }],
            "dimension": {"width": 1080, "height": 1920},
        }
        headers = {"X-Api-Key": self.api_key, "Content-Type": "application/json"}

        with httpx.Client(timeout=60) as c:
            r = c.post(f"{HEYGEN_BASE}/video/generate", json=body, headers=headers)
            r.raise_for_status()
            video_id = r.json()["data"]["video_id"]

            video_url = self._poll(c, video_id, headers)

            out_path = self._save_path(piece)
            with c.stream("GET", video_url) as resp:
                resp.raise_for_status()
                with out_path.open("wb") as f:
                    for chunk in resp.iter_bytes():
                        f.write(chunk)

        assert piece.id is not None
        return RenderedMedia(piece_id=piece.id, video_path=out_path, thumbnail_path=None,
                             brief_path=out_path.with_suffix(".json"), kind="video")

    def _poll(self, client: httpx.Client, video_id: str, headers: dict, timeout: int = 600) -> str:
        deadline = time.time() + timeout
        while time.time() < deadline:
            r = client.get(f"{HEYGEN_BASE}/video_status.get?video_id={video_id}", headers=headers)
            r.raise_for_status()
            data = r.json()["data"]
            if data["status"] == "completed":
                return data["video_url"]
            if data["status"] == "failed":
                raise RuntimeError(f"HeyGen render failed: {data.get('error')}")
            time.sleep(10)
        raise TimeoutError("HeyGen render did not finish in time")

    def _save_path(self, piece: Piece):
        day = datetime.fromtimestamp(piece.created_at).strftime("%Y-%m-%d")
        folder = self.output_dir / day / piece.platform
        folder.mkdir(parents=True, exist_ok=True)
        return folder / f"{piece.slot_time}_{piece.id}.mp4"
