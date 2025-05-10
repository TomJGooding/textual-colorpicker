from textual.app import App, ComposeResult

from textual_colorpicker.hue_picker import HuePicker


class HuePickerApp(App):
    CSS = """
    HuePicker {
        width: 35;
    }
    """

    def compose(self) -> ComposeResult:
        yield HuePicker()


def test_hue_value_is_clamped():
    hue_picker = HuePicker(hue=99.0)
    assert hue_picker.hue == 1.0

    hue_picker.hue = -99.0
    assert hue_picker.hue == 0.0


async def test_clicking_updates_hue_value():
    app = HuePickerApp()
    async with app.run_test() as pilot:
        hue_picker = pilot.app.query_one(HuePicker)
        await pilot.click(HuePicker, offset=(17, 0))
        assert hue_picker.hue == 0.5
