# Autonomous AI Content Agent

A fully autonomous agent that creates, optimizes, and schedules viral short-form and long-form content across TikTok, YouTube, and Instagram.

## Daily output

| Platform  | Count | Slots                                       |
| --------- | ----- | ------------------------------------------- |
| TikTok    | 3     | 09:00, 14:00, 19:00 (local)                 |
| Instagram | 3     | 10:00, 15:00, 20:00 (local)                 |
| YouTube   | 2     | 08:00 (morning), 16:00 (afternoon)          |

## How it works

```
                      ┌──────────────────────────┐
                      │   Scheduler (APScheduler)│
                      └────────────┬─────────────┘
                                   │ fires job
                                   ▼
 ┌──────────────┐    ┌──────────────────────────┐    ┌──────────────┐
 │ Trend miner  │──▶│   Content planner         │──▶│ Script + hook │
 │ (web_search) │    │   (Claude Opus 4.7)       │    │ + caption     │
 └──────────────┘    └────────────┬─────────────┘    └──────┬────────┘
                                   │                         │
                                   ▼                         ▼
                         ┌────────────────┐         ┌─────────────────┐
                         │ Media adapter  │         │ Platform publisher│
                         │ (HeyGen/Runway/│         │ (TikTok/IG/YT)  │
                         │  local ffmpeg) │         └────────┬────────┘
                         └────────┬───────┘                  │
                                  │                          │
                                  └────────┬─────────────────┘
                                           ▼
                                  ┌──────────────────┐
                                  │  Analytics loop  │
                                  │  (feeds next run)│
                                  └──────────────────┘
```

The planner is a single Claude Opus 4.7 call with adaptive thinking + prompt caching. The frozen prefix (brand voice, viral frameworks, hook library) caches across the day; only today's trends + the specific slot (platform/time/theme) are appended after the cache breakpoint.

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env                       # add ANTHROPIC_API_KEY

# Generate one piece of content on demand:
python -m content_agent generate --platform tiktok --dry-run

# Run the full daily schedule:
python -m content_agent run
```

## Configuration

- `config/brand.yaml` — brand voice, niche, target audience, CTAs
- `config/schedule.yaml` — posting times, platform cadence, timezone
- `.env` — API keys (Anthropic, optional platform credentials)

## Platform credentials

The agent runs in **dry-run** mode without platform credentials: it generates the full brief (hook, script, caption, hashtags, thumbnail prompt, publish time) and writes it to SQLite + disk. Add credentials to publish live:

| Env var                     | Used for                    |
| --------------------------- | --------------------------- |
| `ANTHROPIC_API_KEY`         | Claude (required)           |
| `TIKTOK_ACCESS_TOKEN`       | TikTok Content Posting API  |
| `IG_ACCESS_TOKEN` + `IG_USER_ID` | Instagram Graph API    |
| `YT_CLIENT_ID` + `YT_CLIENT_SECRET` + `YT_REFRESH_TOKEN` | YouTube Data API v3 |

## Media generation

Video generation is pluggable via `content_agent/media/`. The default adapter writes a structured brief (no external calls); swap in `HeyGenAdapter`, `RunwayAdapter`, or your own by setting `MEDIA_ADAPTER` in `.env`. See `content_agent/media/base.py` for the interface.

## Layout

```
content_agent/
├── agent.py              # top-level orchestrator
├── scheduler.py          # APScheduler daily jobs
├── llm.py                # Anthropic client (Opus 4.7 + caching)
├── trends.py             # trend discovery (web_search tool)
├── hooks.py              # psychological hook library
├── frameworks.py         # viral content frameworks
├── generation/           # script + caption + hashtag generation
├── media/                # pluggable video adapters
├── platforms/            # TikTok / Instagram / YouTube publishers
├── analytics.py          # performance feedback
└── storage.py            # SQLite state
```
