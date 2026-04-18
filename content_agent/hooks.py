"""Psychological hook library.

These are the opening patterns that stop the scroll in the first 1-3 seconds.
Every hook either triggers curiosity, pattern-interrupts, or promises
asymmetric value. The planner chooses a pattern per piece and Claude fills
in the specifics.

Sources: proven patterns from Alex Hormozi, MrBeast's retention edits,
Nathan Barry's Authority playbook, and what's been demonstrably working on
TikTok/Reels in 2025-2026 (short, high-contrast, concrete).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HookPattern:
    name: str
    template: str
    why_it_works: str
    best_for: tuple[str, ...]  # platform tags: tiktok, reels, shorts, long


HOOK_LIBRARY: tuple[HookPattern, ...] = (
    HookPattern(
        name="contrarian_truth",
        template="Everyone tells you to {common_advice}. That's wrong. Here's what actually works:",
        why_it_works="Pattern-interrupt + authority signal. Triggers the urge to verify.",
        best_for=("tiktok", "reels", "shorts", "long"),
    ),
    HookPattern(
        name="specific_number",
        template="I {did_thing} in {short_timeframe} using {unexpected_tool}. Here's exactly how:",
        why_it_works="Specificity = credibility. Numbers beat adjectives.",
        best_for=("tiktok", "reels", "shorts", "long"),
    ),
    HookPattern(
        name="curiosity_gap",
        template="There's one thing {successful_group} do that nobody talks about. It's not what you think.",
        why_it_works="Open loop. Brain demands closure → watches to the end.",
        best_for=("tiktok", "reels", "shorts"),
    ),
    HookPattern(
        name="before_after",
        template="This is what my {metric} looked like before {change}. And this is after 30 days.",
        why_it_works="Transformation visuals + social proof. Watch-time magnet.",
        best_for=("tiktok", "reels", "shorts", "long"),
    ),
    HookPattern(
        name="insider_secret",
        template="I've worked with {authority_group} for {years}. Here's the one thing they all do:",
        why_it_works="Implies access. Positions you as the filter, not the source.",
        best_for=("tiktok", "reels", "shorts", "long"),
    ),
    HookPattern(
        name="public_mistake",
        template="I wasted {amount} figuring this out. Don't make my mistake:",
        why_it_works="Vulnerability + gift. Converts skeptics fast.",
        best_for=("tiktok", "reels", "shorts", "long"),
    ),
    HookPattern(
        name="loss_aversion",
        template="If you're {doing_common_thing}, you're losing {outcome} every day. Here's the fix:",
        why_it_works="Negativity bias. Loss > gain in attention currency.",
        best_for=("tiktok", "reels", "shorts"),
    ),
    HookPattern(
        name="pattern_interrupt_visual",
        template="[start mid-action, unusual visual or object on screen] 'You're not going to believe what {x} does until you see it.'",
        why_it_works="Visual novelty beats verbal hooks on muted feeds.",
        best_for=("tiktok", "reels", "shorts"),
    ),
    HookPattern(
        name="question_stack",
        template="What if I told you {surprising_claim}? And that {second_claim}? Watch.",
        why_it_works="Stacks curiosity. Commits viewer to the payoff.",
        best_for=("tiktok", "reels", "shorts"),
    ),
    HookPattern(
        name="proof_first",
        template="[show result on screen] Here's {proof}. In this video I'll show you the exact {artifact} I used.",
        why_it_works="Proof up front. Skeptics stay to reverse-engineer.",
        best_for=("tiktok", "reels", "shorts", "long"),
    ),
    HookPattern(
        name="us_vs_them",
        template="The difference between {winners} and {losers} comes down to one habit:",
        why_it_works="Identity framing. Viewers self-select into the winners camp.",
        best_for=("tiktok", "reels", "shorts", "long"),
    ),
    HookPattern(
        name="countdown",
        template="{N} {things} that will {outcome} — the last one is the most important:",
        why_it_works="Retention hack: 'the last one' keeps them watching to the end.",
        best_for=("tiktok", "reels", "shorts", "long"),
    ),
)


def hooks_for_platform(platform: str) -> list[HookPattern]:
    tag = {"tiktok": "tiktok", "instagram": "reels", "youtube_short": "shorts", "youtube_long": "long"}.get(platform, platform)
    return [h for h in HOOK_LIBRARY if tag in h.best_for]


def hook_library_prompt_block() -> str:
    """Serialize the hook library for inclusion in the cached system prompt."""
    lines = ["# HOOK LIBRARY (use these as templates; rewrite, don't copy verbatim)"]
    for h in HOOK_LIBRARY:
        lines.append(f"\n## {h.name}")
        lines.append(f"Template: {h.template}")
        lines.append(f"Why it works: {h.why_it_works}")
        lines.append(f"Best for: {', '.join(h.best_for)}")
    return "\n".join(lines)
