"""Content generation pipeline: hook → script → caption → hashtags."""

from .pieces import generate_piece

__all__ = ["generate_piece"]
