from textual.app import App, ComposeResult
from textual.color import Color
from textual.widgets import Input

from textual_colorpicker.color_inputs import RgbInputs


class RGBInputsApp(App):
    def __init__(self) -> None:
        super().__init__()
        self.messages: list[str] = []

    def compose(self) -> ComposeResult:
        yield RgbInputs()

    def on_rgb_inputs_changed(self, event: RgbInputs.Changed) -> None:
        self.messages.append(event.__class__.__name__)


def test_color_value_is_clamped() -> None:
    rgb_inputs = RgbInputs(Color(999, 999, 999))
    assert rgb_inputs.color == Color(255, 255, 255)

    rgb_inputs.color = Color(-999, -999, -999)
    assert rgb_inputs.color == Color(0, 0, 0)


async def test_updating_inputs_changes_color() -> None:
    app = RGBInputsApp()
    async with app.run_test() as pilot:
        rgb_inputs = pilot.app.query_one(RgbInputs)

        red_input = rgb_inputs.query_one(".--red-input", Input)
        red_input.focus()
        red_input.value = str(128)
        # Test color is updated after input submitted
        await red_input.action_submit()
        await pilot.pause()
        assert rgb_inputs.color == Color(128, 0, 0)

        green_input = rgb_inputs.query_one(".--green-input", Input)
        green_input.focus()
        green_input.value = str(128)
        # Test hsv is updated after input blurred
        green_input.blur()
        await pilot.pause()
        assert rgb_inputs.color == Color(128, 128, 0)

        blue_input = rgb_inputs.query_one(".--blue-input", Input)
        blue_input.value = str(128)
        await blue_input.action_submit()
        await pilot.pause()
        assert rgb_inputs.color == Color(128, 128, 128)


async def test_changed_color_posts_message() -> None:
    app = RGBInputsApp()
    async with app.run_test() as pilot:
        rgb_inputs = pilot.app.query_one(RgbInputs)
        expected_messages: list[str] = []
        assert app.messages == expected_messages

        rgb_inputs.color = Color(0, 255, 255)
        await pilot.pause()
        expected_messages.append("Changed")
        assert app.messages == expected_messages

        red_input = rgb_inputs.query_one(".--red-input", Input)
        red_input.value = str(255)
        await red_input.action_submit()
        await pilot.pause()
        expected_messages.append("Changed")
        assert app.messages == expected_messages


async def test_submitted_value_set_to_zero_if_not_a_number() -> None:
    app = RGBInputsApp()
    async with app.run_test() as pilot:
        rgb_inputs = pilot.app.query_one(RgbInputs)
        red_input = rgb_inputs.query_one(".--red-input", Input)

        red_input.value = "NOT A NUMBER"
        await red_input.action_submit()
        await pilot.pause()

        assert red_input.value == str(0)
        assert rgb_inputs.color == Color(0, 0, 0)
