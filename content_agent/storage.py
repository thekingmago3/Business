"""SQLite DAO for generated pieces, posts, and performance metrics.

The agent uses this to:
- dedupe hooks/angles over a rolling window
- learn from what actually shipped (analytics feedback loop)
- resume after a crash without losing the day's queue
"""

from __future__ import annotations

import json
import sqlite3
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

SCHEMA = """
CREATE TABLE IF NOT EXISTS pieces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at REAL NOT NULL,
    platform TEXT NOT NULL,
    slot_time TEXT NOT NULL,
    theme TEXT NOT NULL,
    length_sec INTEGER NOT NULL,
    format TEXT NOT NULL,
    hook TEXT NOT NULL,
    framework TEXT NOT NULL,
    script_json TEXT NOT NULL,
    caption TEXT NOT NULL,
    hashtags_json TEXT NOT NULL,
    cta TEXT NOT NULL,
    trend_tags_json TEXT NOT NULL,
    media_brief_json TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'drafted'
);

CREATE INDEX IF NOT EXISTS idx_pieces_created ON pieces(created_at);
CREATE INDEX IF NOT EXISTS idx_pieces_platform ON pieces(platform);

CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    piece_id INTEGER NOT NULL REFERENCES pieces(id),
    posted_at REAL NOT NULL,
    platform TEXT NOT NULL,
    external_id TEXT,
    url TEXT,
    dry_run INTEGER NOT NULL DEFAULT 0,
    error TEXT
);

CREATE INDEX IF NOT EXISTS idx_posts_piece ON posts(piece_id);

CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL REFERENCES posts(id),
    fetched_at REAL NOT NULL,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    saves INTEGER DEFAULT 0,
    avg_watch_sec REAL DEFAULT 0,
    followers_gained INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_metrics_post ON metrics(post_id);

CREATE TABLE IF NOT EXISTS trend_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fetched_at REAL NOT NULL,
    platform TEXT NOT NULL,
    payload_json TEXT NOT NULL
);
"""


@dataclass
class Piece:
    id: int | None
    created_at: float
    platform: str
    slot_time: str
    theme: str
    length_sec: int
    format: str
    hook: str
    framework: str
    script: dict[str, Any]
    caption: str
    hashtags: list[str]
    cta: str
    trend_tags: list[str]
    media_brief: dict[str, Any]
    status: str = "drafted"


class Storage:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.executescript(SCHEMA)

    @contextmanager
    def _conn(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def save_piece(self, p: Piece) -> int:
        with self._conn() as c:
            cur = c.execute(
                """INSERT INTO pieces
                   (created_at, platform, slot_time, theme, length_sec, format,
                    hook, framework, script_json, caption, hashtags_json, cta,
                    trend_tags_json, media_brief_json, status)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    p.created_at, p.platform, p.slot_time, p.theme, p.length_sec,
                    p.format, p.hook, p.framework, json.dumps(p.script), p.caption,
                    json.dumps(p.hashtags), p.cta, json.dumps(p.trend_tags),
                    json.dumps(p.media_brief), p.status,
                ),
            )
            return int(cur.lastrowid)

    def recent_hooks(self, platform: str, days: int = 14) -> list[str]:
        cutoff = time.time() - days * 86400
        with self._conn() as c:
            rows = c.execute(
                "SELECT hook FROM pieces WHERE platform=? AND created_at>=?",
                (platform, cutoff),
            ).fetchall()
        return [r["hook"] for r in rows]

    def record_post(
        self,
        piece_id: int,
        platform: str,
        external_id: str | None,
        url: str | None,
        dry_run: bool,
        error: str | None = None,
    ) -> int:
        with self._conn() as c:
            cur = c.execute(
                """INSERT INTO posts
                   (piece_id, posted_at, platform, external_id, url, dry_run, error)
                   VALUES (?,?,?,?,?,?,?)""",
                (piece_id, time.time(), platform, external_id, url, int(dry_run), error),
            )
            c.execute("UPDATE pieces SET status=? WHERE id=?",
                      ("posted" if error is None else "failed", piece_id))
            return int(cur.lastrowid)

    def record_metrics(self, post_id: int, m: dict[str, Any]) -> None:
        with self._conn() as c:
            c.execute(
                """INSERT INTO metrics
                   (post_id, fetched_at, views, likes, comments, shares, saves,
                    avg_watch_sec, followers_gained)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                (
                    post_id, time.time(),
                    m.get("views", 0), m.get("likes", 0), m.get("comments", 0),
                    m.get("shares", 0), m.get("saves", 0),
                    m.get("avg_watch_sec", 0.0), m.get("followers_gained", 0),
                ),
            )

    def top_performers(self, platform: str, limit: int = 10) -> list[dict[str, Any]]:
        """Return highest-engagement pieces with their hook/framework for learning."""
        with self._conn() as c:
            rows = c.execute(
                """SELECT pieces.hook, pieces.framework, pieces.theme,
                          COALESCE(SUM(metrics.views), 0) AS views,
                          COALESCE(SUM(metrics.likes + metrics.comments*3 + metrics.shares*5 + metrics.saves*4), 0) AS engagement
                   FROM pieces
                   JOIN posts ON posts.piece_id = pieces.id
                   LEFT JOIN metrics ON metrics.post_id = posts.id
                   WHERE pieces.platform = ?
                   GROUP BY pieces.id
                   ORDER BY engagement DESC
                   LIMIT ?""",
                (platform, limit),
            ).fetchall()
        return [dict(r) for r in rows]

    def cache_trends(self, platform: str, payload: dict[str, Any]) -> None:
        with self._conn() as c:
            c.execute(
                "INSERT INTO trend_cache (fetched_at, platform, payload_json) VALUES (?,?,?)",
                (time.time(), platform, json.dumps(payload)),
            )

    def latest_trends(self, platform: str, max_age_sec: int = 6 * 3600) -> dict[str, Any] | None:
        cutoff = time.time() - max_age_sec
        with self._conn() as c:
            row = c.execute(
                """SELECT payload_json FROM trend_cache
                   WHERE platform=? AND fetched_at>=?
                   ORDER BY fetched_at DESC LIMIT 1""",
                (platform, cutoff),
            ).fetchone()
        return json.loads(row["payload_json"]) if row else None
