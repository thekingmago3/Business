"""Configuration loading: .env, brand.yaml, schedule.yaml."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"


@dataclass
class SlotSpec:
    time: str
    theme: str
    length_sec: int
    format: str = "short"


@dataclass
class Schedule:
    timezone: str
    tiktok: list[SlotSpec]
    instagram: list[SlotSpec]
    youtube: list[SlotSpec]
    hook_variants_per_piece: int
    use_live_trends: bool

    def slots_for(self, platform: str) -> list[SlotSpec]:
        return {"tiktok": self.tiktok, "instagram": self.instagram, "youtube": self.youtube}[platform]


@dataclass
class Brand:
    name: str
    niche: str
    target_audience: list[str]
    voice_traits: list[str]
    voice_avoid: list[str]
    value_props: list[str]
    ctas: dict[str, list[str]]
    topic_pillars: list[str]
    raw: dict[str, Any] = field(repr=False, default_factory=dict)


@dataclass
class Settings:
    anthropic_api_key: str
    media_adapter: str
    heygen_api_key: str | None
    runway_api_key: str | None
    tiktok_access_token: str | None
    ig_access_token: str | None
    ig_user_id: str | None
    yt_client_id: str | None
    yt_client_secret: str | None
    yt_refresh_token: str | None
    db_path: Path
    output_dir: Path
    dry_run: bool
    timezone: str
    brand: Brand
    schedule: Schedule


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open() as f:
        return yaml.safe_load(f)


def _parse_brand(data: dict[str, Any]) -> Brand:
    voice = data.get("voice", {})
    return Brand(
        name=data["brand_name"],
        niche=data["niche"],
        target_audience=list(data.get("target_audience", [])),
        voice_traits=list(voice.get("traits", [])),
        voice_avoid=list(voice.get("avoid", [])),
        value_props=list(data.get("value_props", [])),
        ctas=dict(data.get("ctas", {})),
        topic_pillars=list(data.get("topic_pillars", [])),
        raw=data,
    )


def _parse_slot(d: dict[str, Any]) -> SlotSpec:
    return SlotSpec(
        time=d["time"],
        theme=d.get("theme", ""),
        length_sec=int(d.get("length_sec", 30)),
        format=d.get("format", "short"),
    )


def _parse_schedule(data: dict[str, Any]) -> Schedule:
    return Schedule(
        timezone=data["timezone"],
        tiktok=[_parse_slot(s) for s in data["tiktok"]["slots"]],
        instagram=[_parse_slot(s) for s in data["instagram"]["slots"]],
        youtube=[_parse_slot(s) for s in data["youtube"]["slots"]],
        hook_variants_per_piece=int(data.get("hook_variants_per_piece", 5)),
        use_live_trends=bool(data.get("use_live_trends", True)),
    )


def load_settings() -> Settings:
    load_dotenv(ROOT / ".env")
    brand = _parse_brand(_load_yaml(CONFIG_DIR / "brand.yaml"))
    schedule = _parse_schedule(_load_yaml(CONFIG_DIR / "schedule.yaml"))

    def env(key: str, default: str | None = None) -> str | None:
        v = os.environ.get(key, default)
        return v if v else None

    return Settings(
        anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
        media_adapter=os.environ.get("MEDIA_ADAPTER", "brief"),
        heygen_api_key=env("HEYGEN_API_KEY"),
        runway_api_key=env("RUNWAY_API_KEY"),
        tiktok_access_token=env("TIKTOK_ACCESS_TOKEN"),
        ig_access_token=env("IG_ACCESS_TOKEN"),
        ig_user_id=env("IG_USER_ID"),
        yt_client_id=env("YT_CLIENT_ID"),
        yt_client_secret=env("YT_CLIENT_SECRET"),
        yt_refresh_token=env("YT_REFRESH_TOKEN"),
        db_path=Path(os.environ.get("CONTENT_AGENT_DB", str(ROOT / "content_agent.db"))),
        output_dir=Path(os.environ.get("CONTENT_AGENT_OUTPUT_DIR", str(ROOT / "output"))),
        dry_run=os.environ.get("DRY_RUN", "true").lower() in ("1", "true", "yes"),
        timezone=os.environ.get("TIMEZONE", schedule.timezone),
        brand=brand,
        schedule=schedule,
    )
