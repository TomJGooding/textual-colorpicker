import pytest
from textual.app import App, ComposeResult
from textual.widgets import Input

from textual_colorpicker.color_inputs import HexInput


class HexInputApp(App):
    def __init__(self) -> None:
        super().__init__()
        self.messages: list[str] = []

    def compose(self) -> ComposeResult:
        yield HexInput()

    def on_hex_input_changed(self, event: HexInput.Changed) -> None:
        self.messages.append(event.__class__.__name__)


def test_invalid_hex_color_raises_exception() -> None:
    hex_input = HexInput()
    with pytest.raises(ValueError):
        hex_input.value = "INVALID"


async def test_input_shows_lowercase_hex_without_prefix() -> None:
    app = HexInputApp()
    async with app.run_test() as pilot:
        hex_input = pilot.app.query_one(HexInput)
        input_widget = hex_input.query_one(Input)

        assert input_widget.value == "ff0000"


async def test_updating_input_changes_hex_value() -> None:
    app = HexInputApp()
    async with app.run_test() as pilot:
        hex_input = pilot.app.query_one(HexInput)
        input_widget = hex_input.query_one(Input)

        # Test value is updated after input submitted
        input_widget.value = "c0c0c0"
        await input_widget.action_submit()
        await pilot.pause()
        assert hex_input.value == "#C0C0C0"

        # Test value is updated after input blurred
        input_widget.value = "a2a2a2"
        input_widget.blur()
        await pilot.pause()
        assert hex_input.value == "#A2A2A2"


async def test_changed_hex_value_posts_message() -> None:
    app = HexInputApp()
    async with app.run_test() as pilot:
        hex_input = pilot.app.query_one(HexInput)
        expected_messages: list[str] = []
        assert app.messages == expected_messages

        hex_input.value = "#00FF00"
        await pilot.pause()
        expected_messages.append("Changed")
        assert app.messages == expected_messages

        input_widget = hex_input.query_one(Input)
        input_widget.value = "0000ff"
        await input_widget.action_submit()
        await pilot.pause()
        expected_messages.append("Changed")
        assert app.messages == expected_messages
