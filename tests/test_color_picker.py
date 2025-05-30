from textual.color import Color

from textual_colorpicker.color_picker import ColorPicker


def test_color_value_is_clamped() -> None:
    color_picker = ColorPicker(Color(999, 999, 999))
    assert color_picker.color == Color(255, 255, 255)

    color_picker.color = Color(-999, -999, -999)
    assert color_picker.color == Color(0, 0, 0)
