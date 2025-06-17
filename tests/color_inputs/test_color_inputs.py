from textual.app import App, ComposeResult
from textual.color import HSV, Color

from textual_colorpicker.color_inputs import ColorInputs, HexInput, HsvInputs, RgbInputs


class ColorInputsApp(App):
    def compose(self) -> ComposeResult:
        yield ColorInputs(Color(0, 255, 255))


def test_color_value_is_clamped() -> None:
    color_inputs = ColorInputs(Color(999, 999, 999))
    assert color_inputs._color == Color(255, 255, 255)

    color_inputs = ColorInputs(Color(-999, -999, -999))
    assert color_inputs._color == Color(0, 0, 0)


async def test_initial_color_updates_all_inputs() -> None:
    app = ColorInputsApp()
    async with app.run_test() as pilot:
        color_inputs = pilot.app.query_one(ColorInputs)

        rgb_inputs = color_inputs.query_one(RgbInputs)
        assert rgb_inputs.color == Color(0, 255, 255)

        hsv_inputs = color_inputs.query_one(HsvInputs)
        assert hsv_inputs.hsv == HSV(0.5, 1.0, 1.0)

        hex_input = color_inputs.query_one(HexInput)
        assert hex_input.value == "#00FFFF"
