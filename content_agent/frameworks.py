"""Viral content frameworks.

A framework is the structural skeleton of a video — hook, setup, payoff,
CTA. Different frameworks fit different slot themes (tutorial vs. story
vs. hot-take). The planner picks one; Claude fleshes it out with
concrete, on-brand beats.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Framework:
    name: str
    beats: tuple[str, ...]
    fits: tuple[str, ...]  # theme tags
    notes: str


FRAMEWORKS: tuple[Framework, ...] = (
    Framework(
        name="PAS",
        beats=(
            "Problem — state the pain in the viewer's exact words",
            "Agitate — twist the knife; make the cost visceral",
            "Solution — present your answer with a single concrete demo",
            "CTA — tell them the one next action",
        ),
        fits=("hook + hot-take", "relatable founder moment", "contrarian"),
        notes="Fastest-converting framework. Best for 30-60s short.",
    ),
    Framework(
        name="AIDA",
        beats=(
            "Attention — open pattern interrupt",
            "Interest — show the unexpected angle",
            "Desire — paint the after state",
            "Action — specific CTA",
        ),
        fits=("tutorial / how-to", "tool teardown"),
        notes="Good for product-adjacent content. Keeps the demo central.",
    ),
    Framework(
        name="story_arc",
        beats=(
            "Status quo — where I was",
            "Inciting incident — what went wrong / what I noticed",
            "Struggle — the failed attempts",
            "Turning point — the realization",
            "Payoff — the result, shown not told",
            "Transferable lesson — what the viewer can steal",
        ),
        fits=("story / behind-the-scenes", "aspirational day-in-the-life"),
        notes="Highest watch-time ceiling. Use for 45-60s+ and long-form.",
    ),
    Framework(
        name="listicle_with_payoff",
        beats=(
            "Hook promising N items with the last being the most valuable",
            "Items 1 to N-1: fast, each with a concrete example",
            "Item N: the unexpected one — slowest, most detail",
            "Summary + save-this CTA",
        ),
        fits=("carousel-style quick win", "tutorial / how-to"),
        notes="Engineered for retention. Great for carousels and Shorts.",
    ),
    Framework(
        name="teardown",
        beats=(
            "Thesis — one sentence on what this tool/workflow does well and where it fails",
            "Demo — 2-3 concrete moves that prove the thesis",
            "Verdict — who should use it, who shouldn't",
            "Adjacent tool mention for credibility",
            "CTA — full breakdown link",
        ),
        fits=("tool teardown in 60s", "tools teardown"),
        notes="Builds authority fast. Name specific products.",
    ),
    Framework(
        name="deep_dive_playbook",
        beats=(
            "Hook — specific outcome + who it's for",
            "Prerequisites — what the viewer needs (30s)",
            "Step-by-step walkthrough (70% of runtime)",
            "Common mistakes section",
            "Results/proof — screenshots, numbers, before/after",
            "Next steps + lead magnet CTA",
        ),
        fits=("deep-dive playbook",),
        notes="Long-form YouTube backbone. Aim 6-10min, chapters enabled.",
    ),
    Framework(
        name="hot_take",
        beats=(
            "Contrarian claim — one sentence, unflinching",
            "Why the mainstream is wrong — evidence",
            "What to do instead — concrete alternative",
            "Anticipated objection + rebuttal",
            "CTA — comment your take",
        ),
        fits=("hook + hot-take", "contrarian"),
        notes="Drives comments (algorithm fuel). Have a real position.",
    ),
)


def frameworks_for_theme(theme: str) -> list[Framework]:
    theme_l = theme.lower()
    matches = [f for f in FRAMEWORKS if any(t in theme_l for t in f.fits)]
    return matches or list(FRAMEWORKS[:3])


def framework_library_prompt_block() -> str:
    lines = ["# CONTENT FRAMEWORKS (pick the best fit for the slot theme)"]
    for f in FRAMEWORKS:
        lines.append(f"\n## {f.name}")
        lines.append("Beats:")
        for b in f.beats:
            lines.append(f"  - {b}")
        lines.append(f"Fits: {', '.join(f.fits)}")
        lines.append(f"Notes: {f.notes}")
    return "\n".join(lines)
