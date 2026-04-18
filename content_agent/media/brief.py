"""Default adapter: serialize the piece to a production-ready brief on disk.

This keeps the agent fully runnable without any video-API keys. The brief
is detailed enough that a human editor or an external video tool can take
it from there.
"""

from __future__ import annotations

import json
from datetime import datetime

from ..storage import Piece
from .base import MediaAdapter, RenderedMedia


class BriefAdapter(MediaAdapter):
    name = "brief"

    def render(self, piece: Piece) -> RenderedMedia:
        day = datetime.fromtimestamp(piece.created_at).strftime("%Y-%m-%d")
        folder = self.output_dir / day / piece.platform
        folder.mkdir(parents=True, exist_ok=True)

        slug = _slug(piece.hook)[:60]
        md_path = folder / f"{piece.slot_time}_{slug}.md"
        json_path = folder / f"{piece.slot_time}_{slug}.json"

        md_path.write_text(_to_markdown(piece), encoding="utf-8")
        json_path.write_text(json.dumps(_to_dict(piece), indent=2), encoding="utf-8")

        assert piece.id is not None
        return RenderedMedia(
            piece_id=piece.id,
            video_path=None,
            thumbnail_path=None,
            brief_path=md_path,
            kind="brief",
        )


def _to_dict(p: Piece) -> dict:
    return {
        "platform": p.platform,
        "slot_time": p.slot_time,
        "theme": p.theme,
        "length_sec": p.length_sec,
        "format": p.format,
        "hook": p.hook,
        "framework": p.framework,
        "script": p.script,
        "caption": p.caption,
        "hashtags": p.hashtags,
        "cta": p.cta,
        "trend_tags": p.trend_tags,
        "media_brief": p.media_brief,
    }


def _to_markdown(p: Piece) -> str:
    beats = p.script.get("beats", [])
    beats_md = "\n".join(
        f"- **{b.get('t_sec','?')}s** — {b.get('line','')}"
        + (f"  \n  _b-roll:_ {b['b_roll']}" if b.get("b_roll") else "")
        for b in beats
    )
    mb = p.media_brief
    return f"""# {p.platform.upper()} @ {p.slot_time} — {p.theme}

**Hook:** {p.hook}
**Framework:** {p.framework}
**Runtime target:** {p.length_sec}s ({p.format})

## Script
{beats_md}

## Caption
{p.caption}

## Hashtags
{' '.join(p.hashtags)}

## CTA
{p.cta}

## Media brief
- Visual style: {mb.get('visual_style','')}
- Pacing: {mb.get('pacing','')}
- Aspect ratio: {mb.get('aspect_ratio','')}
- Music vibe: {mb.get('music_vibe','')}
- On-screen text:
{chr(10).join(f'  - {t}' for t in mb.get('on_screen_text', []))}

## Trend tags
{', '.join(p.trend_tags) or '(none)'}
"""


def _slug(s: str) -> str:
    return "".join(c.lower() if c.isalnum() else "-" for c in s).strip("-")
