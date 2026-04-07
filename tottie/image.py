"""General image utilities for 64×64 LED matrix displays."""

from __future__ import annotations

import struct

from PIL import Image

SIZE = 64


def crop_and_resize(img: Image.Image, size: int = SIZE) -> Image.Image:
    """Centre-crop to square then resize to size×size."""
    w, h = img.size
    m = min(w, h)
    left = (w - m) // 2
    top = (h - m) // 2
    return img.crop((left, top, left + m, top + m)).resize((size, size), Image.LANCZOS)


def to_rgb565(img: Image.Image) -> bytes:
    """Convert a PIL Image to packed RGB565 bytes (big-endian).

    Each pixel becomes 2 bytes: RRRRRGGGGGGBBBBB.
    Suitable for displays that accept raw RGB565 over a serial or network
    transport (e.g. Trinity ESP32 over MQTT).
    """
    w, h = img.size
    buf = bytearray(w * h * 2)
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            struct.pack_into(">H", buf, (y * w + x) * 2, rgb565)
    return bytes(buf)
