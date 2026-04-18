"""Platform publishers: TikTok, Instagram, YouTube.

Publishers are imported lazily so the package works without `httpx` /
`google-api-python-client` when only one platform is in play.
"""

from .base import PublishResult, Publisher


def get_publisher(platform: str, settings) -> Publisher:
    if platform == "tiktok":
        from .tiktok import TikTokPublisher
        return TikTokPublisher(settings)
    if platform == "instagram":
        from .instagram import InstagramPublisher
        return InstagramPublisher(settings)
    if platform == "youtube":
        from .youtube import YouTubePublisher
        return YouTubePublisher(settings)
    raise ValueError(f"unknown platform: {platform}")


__all__ = ["Publisher", "PublishResult", "get_publisher"]
