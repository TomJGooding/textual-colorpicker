from textual.app import App, ComposeResult
from textual.color import HSV, Color

from textual_colorpicker.color_inputs import HexInput, HsvInputs, RgbInputs
from textual_colorpicker.color_picker import ColorPicker
from textual_colorpicker.color_preview import ColorPreview
from textual_colorpicker.hue_picker import HuePicker
from textual_colorpicker.saturation_value_picker import SaturationValuePicker


class ColorPickerApp(App):
    def __init__(self) -> None:
        super().__init__()
        self.messages: list[str] = []

    def compose(self) -> ComposeResult:
        yield ColorPicker()

    def on_color_picker_changed(self, event: HuePicker.Changed) -> None:
        self.messages.append(event.__class__.__name__)


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
        expected_color = Color(0, 255, 255)
        expected_hsv = HSV(0.5, 1.0, 1.0)

        color_preview = pilot.app.query_one(ColorPreview)
        assert color_preview.color == expected_color

        hue_picker = pilot.app.query_one(HuePicker)
        saturation_value_picker = pilot.app.query_one(SaturationValuePicker)
        assert hue_picker.hue == expected_hsv.h
        assert saturation_value_picker.hsv == expected_hsv

        rgb_inputs = pilot.app.query_one(RgbInputs)
        hsv_inputs = pilot.app.query_one(HsvInputs)
        hex_input = pilot.app.query_one(HexInput)
        assert rgb_inputs.color == expected_color
        assert hsv_inputs.hsv == expected_hsv
        assert hex_input.value == expected_color.hex


async def test_changing_hsv_updates_all_widgets() -> None:
    app = ColorPickerApp()
    async with app.run_test() as pilot:
        color_picker = pilot.app.query_one(ColorPicker)

        color_picker._hsv = HSV(0.5, 1.0, 1.0)
        await pilot.pause()
        expected_color = Color(0, 255, 255)
        expected_hsv = HSV(0.5, 1.0, 1.0)

        color_preview = pilot.app.query_one(ColorPreview)
        assert color_preview.color == expected_color

        hue_picker = pilot.app.query_one(HuePicker)
        saturation_value_picker = pilot.app.query_one(SaturationValuePicker)
        assert hue_picker.hue == expected_hsv.h
        assert saturation_value_picker.hsv == expected_hsv

        rgb_inputs = pilot.app.query_one(RgbInputs)
        hsv_inputs = pilot.app.query_one(HsvInputs)
        hex_input = pilot.app.query_one(HexInput)
        assert rgb_inputs.color == expected_color
        assert hsv_inputs.hsv == expected_hsv
        assert hex_input.value == expected_color.hex


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


async def test_updating_rgb_inputs_changes_color() -> None:
    app = ColorPickerApp()
    async with app.run_test() as pilot:
        color_picker = pilot.app.query_one(ColorPicker)
        rgb_inputs = pilot.app.query_one(RgbInputs)

        rgb_inputs.color = Color(0, 255, 255)
        await pilot.pause()

        assert color_picker.color == Color(0, 255, 255)


async def test_updating_hsv_inputs_changes_color() -> None:
    app = ColorPickerApp()
    async with app.run_test() as pilot:
        color_picker = pilot.app.query_one(ColorPicker)
        hsv_inputs = pilot.app.query_one(HsvInputs)

        hsv_inputs.hsv = HSV(0.5, 1.0, 1.0)
        await pilot.pause()

        assert color_picker.color == Color(0, 255, 255)


async def test_updating_hex_input_changes_color() -> None:
    app = ColorPickerApp()
    async with app.run_test() as pilot:
        color_picker = pilot.app.query_one(ColorPicker)
        hex_input = pilot.app.query_one(HexInput)

        hex_input.value = "#00FFFF"
        await pilot.pause()

        assert color_picker.color == Color(0, 255, 255)


async def test_changed_color_posts_message() -> None:
    app = ColorPickerApp()
    async with app.run_test() as pilot:
        color_picker = pilot.app.query_one(ColorPicker)
        expected_messages: list[str] = []
        assert app.messages == expected_messages

        color_picker.color = Color(0, 0, 0)
        await pilot.pause()
        expected_messages.append("Changed")
        assert app.messages == expected_messages

        color_picker._hsv = HSV(1.0, 1.0, 0.0)  # Black
        await pilot.pause()
        # The RGB has not changed so no message should have been posted
        assert color_picker.color == Color(0, 0, 0)
        assert app.messages == expected_messages
