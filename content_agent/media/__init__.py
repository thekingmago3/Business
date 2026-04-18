"""Pluggable media renderers. Default 'brief' writes a shot-list to disk.

HeyGen/Runway adapters are imported lazily so the package works without
`httpx` if you only need the default brief adapter.
"""

from .base import MediaAdapter, RenderedMedia
from .brief import BriefAdapter


def get_adapter(name: str, output_dir, api_keys: dict[str, str | None]) -> MediaAdapter:
    name = (name or "brief").lower()
    if name == "heygen":
        from .heygen import HeyGenAdapter
        return HeyGenAdapter(output_dir=output_dir, api_key=api_keys.get("heygen"))
    if name == "runway":
        from .runway import RunwayAdapter
        return RunwayAdapter(output_dir=output_dir, api_key=api_keys.get("runway"))
    return BriefAdapter(output_dir=output_dir)


__all__ = ["MediaAdapter", "RenderedMedia", "BriefAdapter", "get_adapter"]
