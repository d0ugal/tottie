"""General image utilities for 64×64 LED matrix displays."""

from __future__ import annotations

import numpy as np
from PIL import Image

SIZE = 64


def crop_and_resize(
    img: Image.Image,
    size: int = SIZE,
    anchor: str = "center",
    fit: str = "cover",
    bg: tuple[int, int, int] = (0, 0, 0),
) -> Image.Image:
    """Crop or letterbox to size×size.

    fit controls how the image is fitted to the square target:
      "cover"   — crop to a square at `anchor`, then resize to size×size (default).
                  Fills the target; pixels outside the crop are discarded.
      "contain" — letterbox: scale to fit entirely within size×size preserving
                  aspect ratio, then centre on a `bg`-coloured canvas. `anchor`
                  is ignored.

    anchor (used only when fit="cover") controls which part of the image
    is taken:
      "center"       — centre of the image (default)
      "top_left"     — top-left corner
      "top_right"    — top-right corner
      "bottom_left"  — bottom-left corner
      "bottom_right" — bottom-right corner
    """
    if fit == "contain":
        w, h = img.size
        scale = min(size / w, size / h)
        new_w = max(1, round(w * scale))
        new_h = max(1, round(h * scale))
        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        canvas = Image.new(img.mode, (size, size), bg)
        canvas.paste(resized, ((size - new_w) // 2, (size - new_h) // 2))
        return canvas

    w, h = img.size
    m = min(w, h)
    if anchor == "top_left":
        left, top = 0, 0
    elif anchor == "top_right":
        left, top = w - m, 0
    elif anchor == "bottom_left":
        left, top = 0, h - m
    elif anchor == "bottom_right":
        left, top = w - m, h - m
    else:  # "center" or unknown
        left, top = (w - m) // 2, (h - m) // 2
    return img.crop((left, top, left + m, top + m)).resize(
        (size, size), Image.Resampling.LANCZOS
    )


def to_rgb565(img: Image.Image) -> bytes:
    """Convert a PIL Image to packed RGB565 bytes (big-endian).

    Each pixel becomes 2 bytes: RRRRRGGGGGGBBBBB.
    Suitable for displays that accept raw RGB565 over a serial or network
    transport (e.g. Trinity ESP32 over MQTT).
    """
    arr = np.array(img.convert("RGB"), dtype=np.uint16)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    return rgb565.astype(">u2").tobytes()
