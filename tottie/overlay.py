"""Pixel-font text overlay for 64×64 LED matrix displays.

Ported from tomglenn/idx-ai (MIT). Each glyph is 3×5 pixels encoded as
5 rows of 3-bit bitmasks (MSB = left column).
"""

from __future__ import annotations

from PIL import Image

SIZE = 64
GLYPH_W = 3
GLYPH_H = 5
SPACING = 1  # px gap between characters
CHAR_ADVANCE = GLYPH_W + SPACING  # 4px per character
LINE_SPACING = 7  # px between line baselines (5px glyph + 2px gap)

GLYPHS: dict[str, list[int]] = {
    "0": [0b111, 0b101, 0b101, 0b101, 0b111],
    "1": [0b010, 0b110, 0b010, 0b010, 0b111],
    "2": [0b111, 0b001, 0b111, 0b100, 0b111],
    "3": [0b111, 0b001, 0b111, 0b001, 0b111],
    "4": [0b101, 0b101, 0b111, 0b001, 0b001],
    "5": [0b111, 0b100, 0b111, 0b001, 0b111],
    "6": [0b111, 0b100, 0b111, 0b101, 0b111],
    "7": [0b111, 0b001, 0b001, 0b001, 0b001],
    "8": [0b111, 0b101, 0b111, 0b101, 0b111],
    "9": [0b111, 0b101, 0b111, 0b001, 0b111],
    ":": [0b000, 0b010, 0b000, 0b010, 0b000],
    "A": [0b111, 0b101, 0b111, 0b101, 0b101],
    "B": [0b110, 0b101, 0b110, 0b101, 0b110],
    "C": [0b111, 0b100, 0b100, 0b100, 0b111],
    "D": [0b110, 0b101, 0b101, 0b101, 0b110],
    "E": [0b111, 0b100, 0b110, 0b100, 0b111],
    "F": [0b111, 0b100, 0b110, 0b100, 0b100],
    "G": [0b111, 0b100, 0b101, 0b101, 0b111],
    "H": [0b101, 0b101, 0b111, 0b101, 0b101],
    "I": [0b111, 0b010, 0b010, 0b010, 0b111],
    "J": [0b111, 0b001, 0b001, 0b101, 0b111],
    "K": [0b101, 0b101, 0b110, 0b101, 0b101],
    "L": [0b100, 0b100, 0b100, 0b100, 0b111],
    "M": [0b101, 0b111, 0b111, 0b101, 0b101],
    "N": [0b111, 0b101, 0b101, 0b101, 0b101],
    "O": [0b111, 0b101, 0b101, 0b101, 0b111],
    "P": [0b110, 0b101, 0b110, 0b100, 0b100],
    "Q": [0b111, 0b101, 0b101, 0b111, 0b011],
    "R": [0b110, 0b101, 0b110, 0b101, 0b101],
    "S": [0b111, 0b100, 0b111, 0b001, 0b111],
    "T": [0b111, 0b010, 0b010, 0b010, 0b010],
    "U": [0b101, 0b101, 0b101, 0b101, 0b111],
    "V": [0b101, 0b101, 0b101, 0b101, 0b010],
    "W": [0b101, 0b101, 0b111, 0b111, 0b101],
    "X": [0b101, 0b101, 0b010, 0b101, 0b101],
    "Y": [0b101, 0b101, 0b010, 0b010, 0b010],
    "Z": [0b111, 0b001, 0b010, 0b100, 0b111],
    " ": [0b000, 0b000, 0b000, 0b000, 0b000],
    ".": [0b000, 0b000, 0b000, 0b000, 0b010],
    "-": [0b000, 0b000, 0b111, 0b000, 0b000],
    "'": [0b010, 0b010, 0b000, 0b000, 0b000],
    "!": [0b010, 0b010, 0b010, 0b000, 0b010],
    "?": [0b111, 0b001, 0b011, 0b000, 0b010],
    "&": [0b110, 0b110, 0b011, 0b101, 0b011],
    "+": [0b000, 0b010, 0b111, 0b010, 0b000],
    "/": [0b001, 0b001, 0b010, 0b100, 0b100],
}

MAX_TEXT_WIDTH = SIZE - 2 - 2  # 60px usable
MAX_CHARS = MAX_TEXT_WIDTH // CHAR_ADVANCE  # 15 chars
MAX_INPUT_CHARS = 32
PAGE_CHARS = MAX_CHARS

START_X = 2
START_Y = 2


def _text_width(text: str) -> int:
    if not text:
        return 0
    return len(text) * CHAR_ADVANCE - SPACING


def apply_corner_char(img: Image.Image, char: str, scale: int = 2) -> Image.Image:
    """Draw a single glyph at the bottom-right corner with a darkened background.

    Each glyph pixel is rendered as a scale×scale block (default 2×2).
    """
    lookup = char.upper() if char.isalpha() else char
    rows = GLYPHS.get(lookup)
    if not rows:
        return img

    glyph_w = GLYPH_W * scale
    glyph_h = GLYPH_H * scale
    corner_x = SIZE - glyph_w - START_X
    corner_y = SIZE - glyph_h - START_Y

    pix = img.load()
    assert pix is not None

    for dy in range(-1, glyph_h + 1):
        for dx in range(-1, glyph_w + 1):
            px = corner_x - 1 + dx
            py = corner_y + dy
            if 0 <= px < SIZE and 0 <= py < SIZE:
                r, g, b = pix[px, py]  # type: ignore[misc]
                pix[px, py] = (r >> 2, g >> 2, b >> 2)

    for row_idx, row_bits in enumerate(rows):
        for col in range(GLYPH_W):
            if row_bits & (1 << (GLYPH_W - 1 - col)):
                for sy in range(scale):
                    for sx in range(scale):
                        px = corner_x + col * scale + sx
                        py = corner_y + row_idx * scale + sy
                        if 0 <= px < SIZE and 0 <= py < SIZE:
                            pix[px, py] = (255, 255, 255)

    return img


def apply_now_playing_overlay(
    img: Image.Image,
    track: str,
    artist: str,
    dim: float = 0.5,
    position: str = "top",
) -> Image.Image:
    """Draw darkened background + white pixel-font track/artist text onto img.

    Modifies img in place and returns it.

    dim controls how much of the original pixel brightness is kept behind the
    text (0.0 = black, 1.0 = no change, default 0.5).

    position is "top" (default) or "bottom".
    """
    track_str = track.upper()[:MAX_CHARS]
    artist_str = artist.upper()[:MAX_CHARS]

    if not track_str and not artist_str:
        return img

    n_lines = (1 if track_str else 0) + (1 if artist_str else 0)
    block_h = (LINE_SPACING if n_lines == 2 else 0) + GLYPH_H
    y0 = SIZE - START_Y - block_h if position == "bottom" else START_Y

    pix = img.load()
    assert pix is not None

    def _darken_line(y: int, text_w: int) -> None:
        for dy in range(-1, GLYPH_H + 1):
            for dx in range(-1, text_w + 3):
                px = START_X - 1 + dx
                py = y + dy
                if 0 <= px < SIZE and 0 <= py < SIZE:
                    r, g, b = pix[px, py]  # type: ignore[misc]
                    pix[px, py] = (round(r * dim), round(g * dim), round(b * dim))

    if track_str:
        _darken_line(y0, _text_width(track_str))
    if artist_str:
        _darken_line(y0 + LINE_SPACING, _text_width(artist_str))

    def draw_string(text: str, y: int) -> None:
        cursor_x = START_X
        for ch in text:
            rows = GLYPHS.get(ch)
            if rows is None:
                cursor_x += CHAR_ADVANCE
                continue
            for row_idx, row_bits in enumerate(rows):
                for col in range(GLYPH_W):
                    if row_bits & (1 << (GLYPH_W - 1 - col)):
                        px, py = cursor_x + col, y + row_idx
                        if 0 <= px < SIZE and 0 <= py < SIZE:
                            pix[px, py] = (255, 255, 255)
            cursor_x += CHAR_ADVANCE

    if track_str:
        draw_string(track_str, y0)
    if artist_str:
        draw_string(artist_str, y0 + LINE_SPACING)

    return img


def render_now_playing_frames(
    base_img: Image.Image,
    track: str,
    artist: str,
    page_delay: int = 3000,
    dim: float = 0.5,
    position: str = "top",
) -> list[tuple[Image.Image, int]]:
    """Return (frame, duration_ms) pairs for now-playing display.

    Text is split into pages of PAGE_CHARS characters; both title and artist
    advance to the next page together. A single page produces one static frame;
    multiple pages cycle slowly.

    position is "top" (default) or "bottom"; dim and position are forwarded to
    apply_now_playing_overlay.
    """
    track_upper = track.upper()[:MAX_INPUT_CHARS]
    artist_upper = artist.upper()[:MAX_INPUT_CHARS]

    def _pages(text: str) -> list[str]:
        if not text:
            return [""]
        return [text[i : i + PAGE_CHARS] for i in range(0, len(text), PAGE_CHARS)]

    track_pages = _pages(track_upper)
    artist_pages = _pages(artist_upper)
    n_frames = max(len(track_pages), len(artist_pages))

    frames = []
    for i in range(n_frames):
        t = track_pages[i] if i < len(track_pages) else ""
        a = artist_pages[i] if i < len(artist_pages) else ""
        frame = base_img.copy()
        apply_now_playing_overlay(frame, t, a, dim=dim, position=position)
        frames.append((frame, page_delay))

    return frames
