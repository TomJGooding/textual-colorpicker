from textual.app import App, ComposeResult

from textual_colorpicker.hue_picker import HuePicker


class HuePickerApp(App):
    CSS = """
    HuePicker {
        width: 35;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.messages: list[str] = []

    def compose(self) -> ComposeResult:
        yield HuePicker()

    def on_hue_picker_changed(self, event: HuePicker.Changed) -> None:
        self.messages.append(event.__class__.__name__)


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


async def test_changed_hue_posts_message():
    app = HuePickerApp()
    async with app.run_test() as pilot:
        hue_picker = pilot.app.query_one(HuePicker)
        expected_messages = []
        assert app.messages == expected_messages

        hue_picker.hue = 1.0
        await pilot.pause()
        expected_messages.append("Changed")
        assert app.messages == expected_messages

        await pilot.click(HuePicker, offset=(17, 0))
        expected_messages.append("Changed")
        assert app.messages == expected_messages
