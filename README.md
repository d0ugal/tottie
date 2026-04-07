# tottie

> **Tottie** /ˈtɒti/ — Scottish word meaning *tiny* or *very small*. A tottie wee library for tottie wee displays.

Tottie is a Python library for rendering images onto 64×64 LED matrix displays. It provides the shared rendering primitives used by [`homeassistant-idotmatrix`](https://github.com/d0ugal/iDotMatrix-HomeAssistant) and [`homeassistant-trinity`](https://github.com/d0ugal/homeassistant-trinity).

## What's included

- **`tottie.moon`** — Moon phase renderer. Draws the current moon disc with texture, a direction/altitude ring indicator, and a lunar cycle progress bar across the top edge.
- **`tottie.overlay`** — Pixel-font text overlay. Renders track/artist (or any two lines of text) onto an image using a compact 3×5 bitmap font, with automatic text paging for long strings.
- **`tottie.image`** — Image utilities. Centre-crop-and-resize to any square size, and RGB565 conversion for displays that accept raw pixel data over serial/MQTT.

## Installation

```bash
pip install tottie
```

## Usage

### Moon phase

```python
from tottie import render_moon

img = render_moon(lat="51.5", lon="-0.1", elev=10)
img.save("moon.png")
```

Set `mirror_ew=True` (the default) when the display is on a north-facing wall, so the moon rises on the correct side.

### Now playing overlay

```python
from PIL import Image
from tottie import apply_now_playing_overlay

img = Image.open("album_art.jpg").convert("RGB").resize((64, 64))
apply_now_playing_overlay(img, track="Astronomy", artist="Blue Oyster Cult")
img.save("now_playing.png")
```

For animated paging (long track/artist names scroll across multiple frames):

```python
from tottie import render_now_playing_frames

frames = render_now_playing_frames(img, track="A Very Long Track Title Indeed", artist="Artist")
# frames is a list of (PIL.Image, duration_ms) pairs
```

### Image utilities

```python
from PIL import Image
from tottie import crop_and_resize, to_rgb565

img = Image.open("photo.jpg").convert("RGB")
small = crop_and_resize(img, size=64)   # centre-crop square, resize to 64×64
raw = to_rgb565(small)                  # bytes ready to publish over MQTT
```

## Requirements

- Python 3.11+
- Pillow
- ephem (for moon rendering)

## Licence

MIT
