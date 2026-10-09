"""Images from static/img (see IMAGES.md) with emoji fallbacks when a file is missing.

The app works without a single image: every helper renders a block of the same size with an emoji.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

IMG_DIR = Path(__file__).resolve().parent.parent / "static" / "img"
URL_PREFIX = "app/static/img"


def url(name: str) -> str | None:
    """Static URL for `name` (e.g. "scenes/forest_0"), or None when the file is missing."""
    if (IMG_DIR / f"{name}.webp").is_file():
        return f"{URL_PREFIX}/{name}.webp"
    return None


def _picture(name: str, fallback: str) -> str:
    u = url(name)
    if u:
        return f'<img src="{u}" alt="">'
    return f'<div class="fallback">{escape(fallback)}</div>'


def scene(name: str, fallback: str, overlay: str = "") -> str:
    """Wide scene picture (object-fit: cover, rounded corners, fade-in)."""
    return f'<div class="scene">{_picture(name, fallback)}{overlay}</div>'


def ring_class(approval: float, low: float, high: float) -> str:
    if approval < low:
        return "ring-low"
    if approval <= high:
        return "ring-mid"
    return "ring-high"


def avatar(name: str, fallback: str, approval: float, label: str, low: float = 35,
           high: float = 65) -> str:
    """Round avatar with a coloured approval ring, a short name and the percentage underneath."""
    return (
        f'<div class="avatar"><div class="avatar-pic {ring_class(approval, low, high)}">'
        f"{_picture(name, fallback)}</div>"
        f'<div class="avatar-name">{escape(label)}</div>'
        f'<div class="avatar-pct">{approval:.0f}%</div></div>'
    )


def card(name: str, fallback: str, extra_class: str = "") -> str:
    """Square card picture."""
    return f'<div class="card-pic {extra_class}">{_picture(name, fallback)}</div>'
