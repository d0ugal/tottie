"""Tests for tottie.image utilities."""

import struct

from PIL import Image
from tottie.image import crop_and_resize, to_rgb565


def _solid(color: tuple[int, int, int], size: int = 64) -> Image.Image:
    img = Image.new("RGB", (size, size), color)
    return img


def test_crop_and_resize_square():
    img = Image.new("RGB", (128, 128), (255, 0, 0))
    result = crop_and_resize(img)
    assert result.size == (64, 64)


def test_crop_and_resize_wide():
    img = Image.new("RGB", (200, 100), (0, 255, 0))
    result = crop_and_resize(img)
    assert result.size == (64, 64)


def test_crop_and_resize_tall():
    img = Image.new("RGB", (100, 200), (0, 0, 255))
    result = crop_and_resize(img)
    assert result.size == (64, 64)


def test_crop_and_resize_custom_size():
    img = Image.new("RGB", (128, 128), (255, 255, 0))
    result = crop_and_resize(img, size=32)
    assert result.size == (32, 32)


def test_to_rgb565_length():
    img = _solid((255, 0, 0))
    data = to_rgb565(img)
    assert len(data) == 64 * 64 * 2


def test_to_rgb565_red():
    img = _solid((248, 0, 0))  # pure red in RGB565 (248 = 0xF8, top 5 bits)
    data = to_rgb565(img)
    value = struct.unpack_from(">H", data, 0)[0]
    assert value == 0xF800  # 5 red bits set, all others zero


def test_to_rgb565_white():
    img = _solid((255, 255, 255))
    data = to_rgb565(img)
    value = struct.unpack_from(">H", data, 0)[0]
    assert value == 0xFFFF
