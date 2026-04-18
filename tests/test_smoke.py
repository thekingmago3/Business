"""Smoke tests — run without any API keys.

Exercises the non-network paths: config loading, storage, hook/framework
prompt blocks, brief media adapter, and publisher dry-run.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from content_agent.frameworks import FRAMEWORKS, framework_library_prompt_block, frameworks_for_theme
from content_agent.hooks import HOOK_LIBRARY, hook_library_prompt_block, hooks_for_platform
from content_agent.media.brief import BriefAdapter
from content_agent.platforms.tiktok import TikTokPublisher
from content_agent.storage import Piece, Storage


@pytest.fixture
def tmp_storage(tmp_path):
    return Storage(tmp_path / "test.db")


def _piece(platform: str = "tiktok") -> Piece:
    return Piece(
        id=None,
        created_at=time.time(),
        platform=platform,
        slot_time="09:00",
        theme="hook + hot-take",
        length_sec=30,
        format="short",
        hook="Everyone tells you to grind 14h/day. That's wrong. Here's what actually works:",
        framework="PAS",
        script={"beats": [{"t_sec": 0, "line": "Hook line.", "b_roll": "talking-head"}], "total_runtime_sec": 30},
        caption="The advice nobody gives you.",
        hashtags=["#founder", "#ai", "#productivity"],
        cta="follow for more",
        trend_tags=["AI agents"],
        media_brief={"visual_style": "talking-head", "pacing": "3 cuts per 5s",
                     "on_screen_text": ["grind culture is a trap"], "music_vibe": "lo-fi",
                     "aspect_ratio": "9:16"},
    )


def test_hook_library_has_variety():
    assert len(HOOK_LIBRARY) >= 10
    names = {h.name for h in HOOK_LIBRARY}
    assert len(names) == len(HOOK_LIBRARY)  # no dupes
    assert "contrarian_truth" in names
    assert hooks_for_platform("tiktok")
    assert hook_library_prompt_block().startswith("# HOOK LIBRARY")


def test_framework_library_covers_themes():
    assert len(FRAMEWORKS) >= 5
    assert frameworks_for_theme("hook + hot-take")
    assert frameworks_for_theme("deep-dive playbook")
    assert framework_library_prompt_block().startswith("# CONTENT FRAMEWORKS")


def test_storage_roundtrip(tmp_storage):
    p = _piece()
    pid = tmp_storage.save_piece(p)
    assert pid > 0
    hooks = tmp_storage.recent_hooks("tiktok")
    assert p.hook in hooks
    post_id = tmp_storage.record_post(pid, "tiktok", "ext-1", None, dry_run=True)
    assert post_id > 0
    tmp_storage.record_metrics(post_id, {"views": 1000, "likes": 50, "shares": 5})
    top = tmp_storage.top_performers("tiktok")
    assert top and top[0]["views"] == 1000


def test_trend_cache_ttl(tmp_storage):
    tmp_storage.cache_trends("tiktok", {"rising_topics": [{"topic": "x", "angle": "y"}]})
    latest = tmp_storage.latest_trends("tiktok")
    assert latest and latest["rising_topics"][0]["topic"] == "x"


def test_brief_adapter_writes_artifacts(tmp_path, tmp_storage):
    p = _piece()
    p.id = tmp_storage.save_piece(p)
    adapter = BriefAdapter(output_dir=tmp_path)
    rendered = adapter.render(p)
    assert rendered.brief_path.exists()
    assert rendered.video_path is None
    md = rendered.brief_path.read_text()
    assert p.hook in md
    json_path = rendered.brief_path.with_suffix(".json")
    assert json_path.exists()
    data = json.loads(json_path.read_text())
    assert data["hook"] == p.hook


def test_publisher_dry_run_when_no_creds(tmp_path, tmp_storage):
    class FakeSettings:
        tiktok_access_token = None
        dry_run = True

    p = _piece()
    p.id = tmp_storage.save_piece(p)
    adapter = BriefAdapter(output_dir=tmp_path)
    media = adapter.render(p)

    pub = TikTokPublisher(FakeSettings())
    result = pub.publish(p, media)
    assert result.dry_run is True
    assert result.error is None
