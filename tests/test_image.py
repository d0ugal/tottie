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


def test_contain_wide_letterbox_top_bottom():
    # 200x100 image into 64x64 with contain — scaled to 64x32, padded with 16px
    # black bars above and below.
    img = Image.new("RGB", (200, 100), (255, 0, 0))
    result = crop_and_resize(img, fit="contain")
    assert result.size == (64, 64)
    assert result.getpixel((32, 0)) == (0, 0, 0)  # top bar
    assert result.getpixel((32, 63)) == (0, 0, 0)  # bottom bar
    assert result.getpixel((32, 32)) == (255, 0, 0)  # image centre


def test_contain_tall_pillarbox():
    # 100x200 image into 64x64 with contain — scaled to 32x64, padded with 16px
    # black bars left and right.
    img = Image.new("RGB", (100, 200), (0, 255, 0))
    result = crop_and_resize(img, fit="contain")
    assert result.size == (64, 64)
    assert result.getpixel((0, 32)) == (0, 0, 0)  # left bar
    assert result.getpixel((63, 32)) == (0, 0, 0)  # right bar
    assert result.getpixel((32, 32)) == (0, 255, 0)  # image centre


def test_contain_square_no_bars():
    img = Image.new("RGB", (128, 128), (0, 0, 255))
    result = crop_and_resize(img, fit="contain")
    assert result.size == (64, 64)
    # No padding: every pixel is the source colour.
    assert result.getpixel((0, 0)) == (0, 0, 255)
    assert result.getpixel((63, 63)) == (0, 0, 255)


def test_contain_custom_bg():
    img = Image.new("RGB", (200, 100), (255, 0, 0))
    result = crop_and_resize(img, fit="contain", bg=(50, 100, 150))
    assert result.getpixel((32, 0)) == (50, 100, 150)


def test_contain_ignores_anchor():
    img = Image.new("RGB", (200, 100), (255, 0, 0))
    centred = crop_and_resize(img, fit="contain", anchor="center")
    top_left = crop_and_resize(img, fit="contain", anchor="top_left")
    assert centred.tobytes() == top_left.tobytes()


def test_cover_default_unchanged():
    # Regression: fit defaults to "cover" with anchor-driven behaviour.
    img = Image.new("RGB", (200, 100), (255, 0, 0))
    result = crop_and_resize(img)
    assert result.size == (64, 64)
    # Cover crops to a 100x100 square then resizes; every pixel is red.
    assert result.getpixel((0, 0)) == (255, 0, 0)
    assert result.getpixel((63, 63)) == (255, 0, 0)


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
