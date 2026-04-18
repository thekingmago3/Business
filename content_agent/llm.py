"""Anthropic client wrapper.

All downstream generators (hooks, scripts, captions, analytics) call through
here so we get consistent:
  - model: claude-opus-4-7
  - adaptive thinking (Claude decides depth dynamically)
  - high effort by default; xhigh for heavy generation
  - streaming with .get_final_message() so long generations don't time out
  - prompt caching on the stable system prefix (brand voice + frameworks)
  - JSON extraction helper for structured outputs
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Any

from anthropic import Anthropic

log = logging.getLogger(__name__)

MODEL = "claude-opus-4-7"


@dataclass
class LLMResponse:
    text: str
    usage: dict[str, int]
    stop_reason: str | None


class LLM:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")
        self.client = Anthropic(api_key=api_key)

    def generate(
        self,
        system: str,
        user: str,
        *,
        max_tokens: int = 4096,
        effort: str = "high",
        cache_system: bool = True,
        tools: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        """Single-turn generation with streaming and prompt caching.

        System prompt gets an ephemeral cache breakpoint so the stable
        brand/framework prefix is reused across the day's ~8 generations.
        """
        system_blocks: list[dict[str, Any]] = [{"type": "text", "text": system}]
        if cache_system:
            system_blocks[0]["cache_control"] = {"type": "ephemeral"}

        kwargs: dict[str, Any] = {
            "model": MODEL,
            "max_tokens": max_tokens,
            "system": system_blocks,
            "messages": [{"role": "user", "content": user}],
            "thinking": {"type": "adaptive"},
            "output_config": {"effort": effort},
        }
        if tools:
            kwargs["tools"] = tools

        with self.client.messages.stream(**kwargs) as stream:
            final = stream.get_final_message()

        text_parts = [b.text for b in final.content if getattr(b, "type", None) == "text"]
        usage = {
            "input_tokens": final.usage.input_tokens,
            "output_tokens": final.usage.output_tokens,
            "cache_read_input_tokens": getattr(final.usage, "cache_read_input_tokens", 0) or 0,
            "cache_creation_input_tokens": getattr(final.usage, "cache_creation_input_tokens", 0) or 0,
        }
        if usage["cache_read_input_tokens"] == 0 and cache_system:
            log.debug("No prompt-cache hit on this call (expected on first run of the day).")
        return LLMResponse(text="\n".join(text_parts).strip(), usage=usage, stop_reason=final.stop_reason)

    def generate_json(
        self,
        system: str,
        user: str,
        *,
        max_tokens: int = 4096,
        effort: str = "high",
    ) -> Any:
        """Generate and parse JSON. Retries once on parse failure with a stricter nudge."""
        resp = self.generate(
            system=system + "\n\nYou MUST respond with valid JSON only. No prose before or after.",
            user=user,
            max_tokens=max_tokens,
            effort=effort,
        )
        try:
            return _extract_json(resp.text)
        except ValueError:
            log.warning("JSON parse failed, retrying with stricter instruction.")
            resp = self.generate(
                system=system + "\n\nRespond with ONLY a JSON document. No markdown. No commentary.",
                user=user + "\n\nReturn JSON only.",
                max_tokens=max_tokens,
                effort=effort,
            )
            return _extract_json(resp.text)


_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)


def _extract_json(text: str) -> Any:
    """Pull a JSON object/array out of Claude's response, fence-tolerant."""
    text = text.strip()
    m = _FENCE.search(text)
    if m:
        text = m.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        first = min((i for i in (text.find("{"), text.find("[")) if i >= 0), default=-1)
        last = max(text.rfind("}"), text.rfind("]"))
        if first >= 0 and last > first:
            return json.loads(text[first:last + 1])
        raise ValueError(f"No JSON found in response: {text[:200]}")
