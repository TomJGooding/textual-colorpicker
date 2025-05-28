import pytest

from textual_colorpicker.color_inputs import HexInput


def test_invalid_hex_color_raises_exception() -> None:
    hex_input = HexInput()
    with pytest.raises(ValueError):
        hex_input.value = "INVALID"
