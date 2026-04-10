"""General image utilities for 64×64 LED matrix displays."""

from __future__ import annotations

import struct
from typing import cast

from PIL import Image

SIZE = 64


def crop_and_resize(
    img: Image.Image,
    size: int = SIZE,
    anchor: str = "center",
) -> Image.Image:
    """Crop to a square region then resize to size×size.

    anchor controls which part of the image is taken:
      "center"       — centre of the image (default)
      "top_left"     — top-left corner
      "top_right"    — top-right corner
      "bottom_left"  — bottom-left corner
      "bottom_right" — bottom-right corner
    """
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
    rgb = img.convert("RGB")
    w, h = rgb.size
    buf = bytearray(w * h * 2)
    for y in range(h):
        for x in range(w):
            r, g, b = cast(tuple[int, int, int], rgb.getpixel((x, y)))
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            struct.pack_into(">H", buf, (y * w + x) * 2, rgb565)
    return bytes(buf)
