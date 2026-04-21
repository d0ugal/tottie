"""Tests for tottie.overlay."""

from PIL import Image
from tottie.overlay import apply_corner_char, apply_now_playing_overlay, render_now_playing_frames


def _black() -> Image.Image:
    return Image.new("RGB", (64, 64), (0, 0, 0))


def test_apply_overlay_returns_image():
    img = _black()
    result = apply_now_playing_overlay(img, "Track", "Artist")
    assert result is img  # modified in place


def test_apply_overlay_empty_strings():
    img = _black()
    result = apply_now_playing_overlay(img, "", "")
    assert result is img


def test_apply_overlay_writes_pixels():
    img = _black()
    apply_now_playing_overlay(img, "A", "")
    # At least one pixel should be white (the glyph)
    pixels = [img.getpixel((x, y)) for x in range(img.width) for y in range(img.height)]
    assert any(p == (255, 255, 255) for p in pixels)


def test_render_now_playing_frames_single():
    img = _black()
    frames = render_now_playing_frames(img, "Short", "Artist")
    assert len(frames) == 1
    frame, duration = frames[0]
    assert isinstance(frame, Image.Image)
    assert duration == 3000


def test_render_now_playing_frames_paging():
    img = _black()
    # 16 chars > PAGE_CHARS (15), so should produce 2 pages
    frames = render_now_playing_frames(img, "A" * 16, "")
    assert len(frames) == 2


def test_render_now_playing_frames_custom_delay():
    img = _black()
    frames = render_now_playing_frames(img, "Track", "Artist", page_delay=1000)
    _, duration = frames[0]
    assert duration == 1000


def test_apply_corner_char_returns_image():
    img = _black()
    result = apply_corner_char(img, "+")
    assert result is img


def test_apply_corner_char_writes_pixels():
    img = _black()
    apply_corner_char(img, "+")
    pixels = [img.getpixel((x, y)) for x in range(img.width) for y in range(img.height)]
    assert any(p == (255, 255, 255) for p in pixels)


def test_apply_corner_char_minus():
    img = _black()
    result = apply_corner_char(img, "-")
    assert result is img


def test_apply_corner_char_unknown_skips():
    img = _black()
    result = apply_corner_char(img, "~")
    assert result is img
    pixels = [img.getpixel((x, y)) for x in range(img.width) for y in range(img.height)]
    assert not any(p == (255, 255, 255) for p in pixels)


def test_apply_corner_char_empty_skips():
    img = _black()
    result = apply_corner_char(img, "")
    assert result is img
