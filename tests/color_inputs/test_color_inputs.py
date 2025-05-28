from textual_colorpicker.color_inputs import ColorInputs
from textual.color import Color


def test_color_value_is_clamped() -> None:
    color_inputs = ColorInputs(Color(999, 999, 999))
    assert color_inputs.color == Color(255, 255, 255)

    color_inputs.color = Color(-999, -999, -999)
    assert color_inputs.color == Color(0, 0, 0)
