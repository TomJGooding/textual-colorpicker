from textual.app import App, ComposeResult
from textual.color import HSV, Color

from textual_colorpicker.color_inputs import ColorInputs
from textual_colorpicker.color_picker import ColorPicker
from textual_colorpicker.color_preview import ColorPreview
from textual_colorpicker.hue_picker import HuePicker
from textual_colorpicker.saturation_value_picker import SaturationValuePicker


class ColorPickerApp(App):
    def compose(self) -> ComposeResult:
        yield ColorPicker()


def test_color_value_is_clamped() -> None:
    color_picker = ColorPicker(Color(999, 999, 999))
    assert color_picker.color == Color(255, 255, 255)

    color_picker.color = Color(-999, -999, -999)
    assert color_picker.color == Color(0, 0, 0)


async def test_changing_color_updates_all_widgets() -> None:
    app = ColorPickerApp()
    async with app.run_test() as pilot:
        color_picker = pilot.app.query_one(ColorPicker)

        color_picker.color = Color(0, 255, 255)
        await pilot.pause()

        color_preview = pilot.app.query_one(ColorPreview)
        assert color_preview.color == Color(0, 255, 255)

        color_inputs = pilot.app.query_one(ColorInputs)
        assert color_inputs.color == Color(0, 255, 255)

        hue_picker = pilot.app.query_one(HuePicker)
        assert hue_picker.hue == 0.5

        saturation_value_picker = pilot.app.query_one(SaturationValuePicker)
        assert saturation_value_picker.hsv == HSV(0.5, 1.0, 1.0)


async def test_updating_color_inputs_changes_color() -> None:
    app = ColorPickerApp()
    async with app.run_test() as pilot:
        color_picker = pilot.app.query_one(ColorPicker)
        color_inputs = pilot.app.query_one(ColorInputs)

        color_inputs.color = Color(128, 0, 0)
        await pilot.pause()

        assert color_picker.color == Color(128, 0, 0)


async def test_updating_hue_picker_changes_color() -> None:
    app = ColorPickerApp()
    async with app.run_test() as pilot:
        color_picker = pilot.app.query_one(ColorPicker)
        hue_picker = pilot.app.query_one(HuePicker)

        hue_picker.hue = 0.5
        await pilot.pause()

        assert color_picker.color == Color(0, 255, 255)


async def test_updating_saturation_value_picker_changes_color() -> None:
    app = ColorPickerApp()
    async with app.run_test() as pilot:
        color_picker = pilot.app.query_one(ColorPicker)
        saturation_value_picker = pilot.app.query_one(SaturationValuePicker)

        saturation_value_picker.hsv = HSV(0.0, 0.0, 1.0)
        await pilot.pause()

        assert color_picker.color == Color(255, 255, 255)
