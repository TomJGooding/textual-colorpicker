from colorsys import hsv_to_rgb, rgb_to_hsv

from textual.color import HSV, Color

# NOTE: Currently Textual's `Color` class is missing HSV support.
# I've submitted a pull request to add a `Color.hsv` property and
# `Color.from_hsv` class method here:
# https://github.com/Textualize/textual/pull/5803


def _hsv_from_color(color: Color) -> HSV:
    r, g, b = color.normalized
    h, s, v = rgb_to_hsv(r, g, b)
    return HSV(h, s, v)


def _color_from_hsv(h: float, s: float, v: float) -> Color:
    r, g, b = hsv_to_rgb(h, s, v)
    return Color(int(r * 255 + 0.5), int(g * 255 + 0.5), int(b * 255 + 0.5))
