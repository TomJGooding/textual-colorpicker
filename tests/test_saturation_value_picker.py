from textual.app import App, ComposeResult
from textual.color import HSV

from textual_colorpicker.saturation_value_picker import SaturationValuePicker


class SaturationValuePickerApp(App):
    CSS = """
    SaturationValuePicker {
        width: 35;
        height: 17;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.messages: list[str] = []

    def compose(self) -> ComposeResult:
        yield SaturationValuePicker()

    def on_saturation_value_picker_changed(
        self, event: SaturationValuePicker.Changed
    ) -> None:
        self.messages.append(event.__class__.__name__)


def test_hsv_value_is_clamped():
    saturation_value_picker = SaturationValuePicker(HSV(99.0, 99.0, 99.0))
    assert saturation_value_picker.hsv == HSV(1.0, 1.0, 1.0)

    saturation_value_picker.hsv = HSV(-99.0, -99.0, -99.0)
    assert saturation_value_picker.hsv == HSV(0.0, 0.0, 0.0)


async def test_clicking_updates_hsv_value():
    app = SaturationValuePickerApp()
    async with app.run_test() as pilot:
        saturation_value_picker = pilot.app.query_one(SaturationValuePicker)
        await pilot.click(SaturationValuePicker, offset=(17, 8))
        assert saturation_value_picker.hsv.s == 0.5
        assert saturation_value_picker.hsv.v == 0.5


async def test_clicking_outside_content_is_noop():
    app = SaturationValuePickerApp()
    async with app.run_test() as pilot:
        saturation_value_picker = pilot.app.query_one(SaturationValuePicker)
        saturation_value_picker.styles.padding = (0, 2)
        expected_hsv = HSV(0.0, 1.0, 1.0)
        assert saturation_value_picker.hsv == expected_hsv  # Sanity check

        await pilot.click(SaturationValuePicker, offset=(1, 0))
        assert saturation_value_picker.hsv == expected_hsv  # No change

        await pilot.click(SaturationValuePicker, offset=(33, 0))
        assert saturation_value_picker.hsv == expected_hsv  # No change


async def test_changed_hsv_posts_message():
    app = SaturationValuePickerApp()
    async with app.run_test() as pilot:
        saturation_value_picker = pilot.app.query_one(SaturationValuePicker)
        expected_messages = []
        assert app.messages == expected_messages

        saturation_value_picker.hsv = HSV(0.0, 0.0, 0.0)
        await pilot.pause()
        expected_messages.append("Changed")
        assert app.messages == expected_messages

        await pilot.click(SaturationValuePicker, offset=(17, 8))
        expected_messages.append("Changed")
        assert app.messages == expected_messages
