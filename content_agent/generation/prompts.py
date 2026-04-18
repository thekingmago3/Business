"""System-prompt construction.

The cached prefix is: brand voice + hook library + framework library +
top-performer learnings. These are stable across a day's ~8 generations,
so the first call pays tokens and the rest read from cache.

The user message is: today's trends + this specific slot spec.
"""

from __future__ import annotations

from typing import Any

from ..config import Brand, SlotSpec
from ..frameworks import framework_library_prompt_block
from ..hooks import hook_library_prompt_block


def build_system_prompt(brand: Brand, top_performers: list[dict[str, Any]] | None = None) -> str:
    """Stable, cache-friendly system prompt. Order matters — keep volatile bits out."""
    sections: list[str] = []

    sections.append(
        "You are a world-class short-form content strategist and copywriter. "
        "You write for creators who need to STOP THE SCROLL in 1-3 seconds, "
        "hold attention for the full runtime, and convert viewers into followers. "
        "You understand the TikTok, Instagram Reels, and YouTube algorithms at a "
        "practitioner level — retention, shares, and comments are what you optimize for, "
        "in that order."
    )

    sections.append(f"""# BRAND
Name: {brand.name}
Niche: {brand.niche}
Target audience:
{_bullets(brand.target_audience)}

Voice traits:
{_bullets(brand.voice_traits)}

Voice AVOID list (do not use):
{_bullets(brand.voice_avoid)}

Value props (pick one that fits, don't cram all in):
{_bullets(brand.value_props)}

Topic pillars:
{_bullets(brand.topic_pillars)}""")

    sections.append(hook_library_prompt_block())
    sections.append(framework_library_prompt_block())

    sections.append("""# OUTPUT DISCIPLINE
- Every script must be performable at natural pace within the specified length_sec.
  Budget ~2.5 words per second of runtime.
- Hook must land by second 2. Promise must pay off by the end.
- Use concrete specifics: numbers, tools, dollar amounts, timeframes. No vague claims.
- Never use the brand's AVOID words.
- One CTA per piece. Pick from the brand's CTA bank or write a tighter variant.
- Captions: platform-native. TikTok/Reels = short and punchy (≤200 chars). YouTube long = 2-3 para with chapter timestamps.
- Hashtags: 3-5 tight, relevant tags. No spammy walls.""")

    if top_performers:
        sections.append("# LEARNINGS FROM TOP PERFORMERS (reuse what's working)")
        for p in top_performers[:5]:
            sections.append(
                f"- hook={p.get('hook','')[:100]!r} framework={p.get('framework')} "
                f"theme={p.get('theme')} engagement={p.get('engagement',0)}"
            )

    return "\n\n".join(sections)


def build_user_prompt(
    platform: str,
    slot: SlotSpec,
    trends_block: str,
    recent_hooks: list[str],
    hook_variants: int,
) -> str:
    """Volatile portion: today's trends + slot spec. Kept AFTER the cached prefix."""
    recent = "\n".join(f"- {h!r}" for h in recent_hooks[-20:]) or "(none yet)"
    return f"""{trends_block}

# SLOT
Platform: {platform}
Time (local): {slot.time}
Theme: {slot.theme}
Length: {slot.length_sec} seconds
Format: {slot.format}

# RECENT HOOKS WE'VE USED (do NOT repeat these angles)
{recent}

# TASK
Generate ONE piece of content for this slot. Return a single JSON object matching:

{{
  "hook": "<the winning hook, ≤18 words, ready to say on camera>",
  "hook_variants": [ "<{hook_variants-1} alternates, different patterns, same promise>" ],
  "framework": "<the name of the framework you're using>",
  "script": {{
    "beats": [
      {{"t_sec": 0, "line": "<on-camera line>", "b_roll": "<visual / b-roll note>"}}
    ],
    "total_runtime_sec": <int>
  }},
  "caption": "<platform-native caption>",
  "hashtags": ["#tag1", "#tag2", "#tag3"],
  "cta": "<one clear next-action>",
  "trend_tags": ["<which rising_topics or formats you used, if any>"],
  "media_brief": {{
    "visual_style": "<e.g. talking-head w/ bold captions, screen recording, cinematic day-in-the-life>",
    "pacing": "<cuts per 5s>",
    "on_screen_text": ["<punchy frames to overlay>"],
    "music_vibe": "<e.g. lo-fi house, upbeat chill, trending audio if specified>",
    "aspect_ratio": "<9:16 | 16:9>"
  }}
}}

Write like the brand. Be specific. Don't hedge. No corporate-speak."""


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {i}" for i in items) if items else "- (none)"
