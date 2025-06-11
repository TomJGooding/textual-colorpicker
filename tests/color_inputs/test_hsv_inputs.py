from textual.app import App, ComposeResult
from textual.color import HSV
from textual.widgets import Input

from textual_colorpicker.color_inputs import HsvInputs


class HSVInputsApp(App):
    def __init__(self) -> None:
        super().__init__()
        self.messages: list[str] = []

    def compose(self) -> ComposeResult:
        yield HsvInputs()

    def on_hsv_inputs_changed(self, event: HsvInputs.Changed) -> None:
        self.messages.append(event.__class__.__name__)


def test_hsv_value_is_clamped() -> None:
    hsv_inputs = HsvInputs(HSV(99.0, 99.0, 99.0))
    assert hsv_inputs.hsv == HSV(1.0, 1.0, 1.0)

    hsv_inputs.hsv = HSV(-99.0, -99.0, -99.0)
    assert hsv_inputs.hsv == HSV(0.0, 0.0, 0.0)


async def test_inputs_show_scaled_hsv_values() -> None:
    app = HSVInputsApp()
    async with app.run_test() as pilot:
        hsv_inputs = pilot.app.query_one(HsvInputs)
        hue_input = hsv_inputs.query_one(".--hue-input", Input)
        saturation_input = hsv_inputs.query_one(".--saturation-input", Input)
        value_input = hsv_inputs.query_one(".--value-input", Input)

        assert hue_input.value == str(0)
        assert saturation_input.value == str(100)
        assert value_input.value == str(100)


async def test_changing_hsv_updates_all_inputs() -> None:
    app = HSVInputsApp()
    async with app.run_test() as pilot:
        hsv_inputs = pilot.app.query_one(HsvInputs)
        hue_input = hsv_inputs.query_one(".--hue-input", Input)
        saturation_input = hsv_inputs.query_one(".--saturation-input", Input)
        value_input = hsv_inputs.query_one(".--value-input", Input)

        hsv_inputs.hsv = HSV(0.1, 0.1, 0.1)
        await pilot.pause()

        assert hue_input.value == str(36)
        assert saturation_input.value == str(10)
        assert value_input.value == str(10)


async def test_updating_inputs_changes_hsv() -> None:
    app = HSVInputsApp()
    async with app.run_test() as pilot:
        hsv_inputs = pilot.app.query_one(HsvInputs)

        hue_input = hsv_inputs.query_one(".--hue-input", Input)
        hue_input.focus()
        hue_input.value = str(36)
        # Test hsv is updated after input submitted
        await hue_input.action_submit()
        await pilot.pause()
        assert hsv_inputs.hsv == HSV(0.1, 1.0, 1.0)

        saturation_input = hsv_inputs.query_one(".--saturation-input", Input)
        saturation_input.focus()
        saturation_input.value = str(10)
        # Test hsv is updated after input blurred
        saturation_input.blur()
        await pilot.pause()
        assert hsv_inputs.hsv == HSV(0.1, 0.1, 1.0)

        value_input = hsv_inputs.query_one(".--value-input", Input)
        value_input.value = str(10)
        await value_input.action_submit()
        await pilot.pause()
        assert hsv_inputs.hsv == HSV(0.1, 0.1, 0.1)


async def test_changed_hsv_posts_message() -> None:
    app = HSVInputsApp()
    async with app.run_test() as pilot:
        hsv_inputs = pilot.app.query_one(HsvInputs)
        expected_messages: list[str] = []
        assert app.messages == expected_messages

        hsv_inputs.hsv = HSV(0.1, 0.1, 0.1)
        await pilot.pause()
        expected_messages.append("Changed")
        assert app.messages == expected_messages


async def test_submitted_value_set_to_zero_if_not_a_number() -> None:
    app = HSVInputsApp()
    async with app.run_test() as pilot:
        hsv_inputs = pilot.app.query_one(HsvInputs)
        saturation_input = hsv_inputs.query_one(".--saturation-input", Input)

        saturation_input.value = "NOT A NUMBER"
        await saturation_input.action_submit()
        await pilot.pause()

        assert saturation_input.value == str(0)
        assert hsv_inputs.hsv == HSV(0.0, 0.0, 1.0)


async def test_submitted_value_rounded_if_float() -> None:
    app = HSVInputsApp()
    async with app.run_test() as pilot:
        hsv_inputs = pilot.app.query_one(HsvInputs)
        value_input = hsv_inputs.query_one(".--value-input", Input)

        value_input.value = str(50.2)
        await value_input.action_submit()
        await pilot.pause()

        assert value_input.value == str(50)
        assert hsv_inputs.hsv == HSV(0.0, 1.0, 0.5)


async def test_submitted_value_clamped_if_not_in_range() -> None:
    app = HSVInputsApp()
    async with app.run_test() as pilot:
        hsv_inputs = pilot.app.query_one(HsvInputs)
        saturation_input = hsv_inputs.query_one(".--saturation-input", Input)

        saturation_input.value = str(999)
        await saturation_input.action_submit()
        await pilot.pause()
        assert saturation_input.value == str(100)
        assert hsv_inputs.hsv == HSV(0.0, 1.0, 1.0)

        saturation_input.value = str(-999)
        await saturation_input.action_submit()
        await pilot.pause()
        assert saturation_input.value == str(0)
        assert hsv_inputs.hsv == HSV(0.0, 0.0, 1.0)
