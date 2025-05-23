from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.color import HSV, Color
from textual.containers import HorizontalGroup
from textual.geometry import clamp
from textual.message import Message
from textual.reactive import var
from textual.validation import Integer
from textual.widget import Widget
from textual.widgets import Input, Label

from textual_colorpicker._color_hsv import _hsv_from_color


class RgbInputs(Widget):
    DEFAULT_CSS = """
    RgbInputs {
        width: auto;
        height: auto;

        HorizontalGroup {
            width: auto;
        }

        Label {
            padding: 1 0;
        }

        Input {
            width: 10;
        }
    }
    """

    color: var[Color] = var(Color(255, 0, 0), init=False)

    class Changed(Message):
        def __init__(self, rgb_inputs: RgbInputs, color: Color) -> None:
            super().__init__()
            self.color: Color = color
            self.rgb_inputs: RgbInputs = rgb_inputs

        @property
        def control(self) -> RgbInputs:
            return self.rgb_inputs

    def compose(self) -> ComposeResult:
        r, g, b = self.color.rgb
        with HorizontalGroup():
            yield Label("R:")
            yield Input(
                str(r),
                validators=Integer(0, 255),
                id="--red-input",
            )
        with HorizontalGroup():
            yield Label("G:")
            yield Input(
                str(g),
                validators=Integer(0, 255),
                id="--green-input",
            )
        with HorizontalGroup():
            yield Label("B:")
            yield Input(
                str(b),
                validators=Integer(0, 255),
                id="--blue-input",
            )

    def validate_color(self, color: Color) -> Color:
        return color.clamped

    def watch_color(self) -> None:
        self._update_all_from_color(self.color)

        self.post_message(self.Changed(self, self.color))

    def _update_all_from_color(self, color: Color) -> None:
        red_input = self.query_one("#--red-input", Input)
        green_input = self.query_one("#--green-input", Input)
        blue_input = self.query_one("#--blue-input", Input)

        clamped_color = color.clamped
        r, g, b = clamped_color.rgb

        red_input.value = str(r)
        green_input.value = str(g)
        blue_input.value = str(b)

        # Force a re-validation of the input selections.
        # Workaround for https://github.com/Textualize/textual/issues/5811
        red_input.selection = red_input.selection
        green_input.selection = green_input.selection
        blue_input.selection = blue_input.selection

    @on(Input.Blurred)
    @on(Input.Submitted)
    def _on_input_blurred_or_submitted(
        self, event: Input.Blurred | Input.Submitted
    ) -> None:
        event.stop()
        validation_result = event.validation_result
        assert validation_result is not None
        # If the value is not a number, set the input to zero.
        if not validation_result.is_valid:
            if any(
                isinstance(failure, Integer.NotANumber)
                for failure in validation_result.failures
            ):
                event.input.value = str(0)

        # If the value is a float, round to the nearest integer.
        r = int(float(self.query_one("#--red-input", Input).value) + 0.5)
        g = int(float(self.query_one("#--green-input", Input).value) + 0.5)
        b = int(float(self.query_one("#--blue-input", Input).value) + 0.5)

        clamped_color = Color(r, g, b).clamped
        # If the value is not in range, set the input to the clamped value.
        self._update_all_from_color(clamped_color)

        self.color = clamped_color


class HsvInputs(Widget):
    DEFAULT_CSS = """
    HsvInputs {
        width: auto;
        height: auto;

        HorizontalGroup {
            width: auto;
        }

        Label {
            padding: 1 0;
        }

        Input {
            width: 10;
        }
    }
    """

    hsv: var[HSV] = var(HSV(0.0, 1.0, 1.0), init=False)

    def compose(self) -> ComposeResult:
        h, s, v = self.hsv_integer_values
        with HorizontalGroup():
            yield Label("H:")
            yield Input(str(h), id="--hue-input")
        with HorizontalGroup():
            yield Label("S:")
            yield Input(str(s), id="--saturation-input")
        with HorizontalGroup():
            yield Label("V:")
            yield Input(str(v), id="--value-input")

    def validate_hsv(self, hsv: HSV) -> HSV:
        h, s, v = hsv

        clamped_hsv = HSV(
            clamp(h, 0.0, 1.0),
            clamp(s, 0.0, 1.0),
            clamp(v, 0.0, 1.0),
        )

        return clamped_hsv

    def watch_hsv(self) -> None:
        h, s, v = self.hsv_integer_values
        self.query_one("#--hue-input", Input).value = str(h)
        self.query_one("#--saturation-input", Input).value = str(s)
        self.query_one("#--value-input", Input).value = str(v)

    @property
    def hsv_integer_values(self) -> tuple[int, int, int]:
        h = int(self.hsv.h * 360 + 0.5)
        s = int(self.hsv.s * 100 + 0.5)
        v = int(self.hsv.v * 100 + 0.5)
        return (h, s, v)


class HexInput(Widget):
    DEFAULT_CSS = """
    HexInput {
        width: auto;
        height: auto;

        HorizontalGroup {
            width: auto;
        }

        Label {
            padding: 1 0;
        }

        Input {
            width: 13;
        }
    }
    """

    value: var[str] = var("ff0000", init=False)

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label("#")
            yield Input(self.value)

    def _watch_value(self, value: str) -> None:
        self.query_one(Input).value = value


class ColorInputs(Widget):
    DEFAULT_CSS = """
    ColorInputs {
        width: auto;
        height: auto;

        HorizontalGroup {
            width: auto;
        }

        HexInput {
            margin-top: 1;
            margin-left: 1;
        }
    }
    """

    color: var[Color] = var(Color(255, 0, 0), init=False)

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield RgbInputs()
            yield HsvInputs(disabled=True)
        yield HexInput(disabled=True)

    def watch_color(self) -> None:
        h, s, v = _hsv_from_color(self.color)
        hex_value = self.color.hex.lower().lstrip("#")
        self.query_one(RgbInputs).color = self.color
        self.query_one(HsvInputs).hsv = HSV(h, s, v)
        self.query_one(HexInput).value = hex_value

    def _on_rgb_inputs_changed(self, event: RgbInputs.Changed) -> None:
        self.color = event.color


if __name__ == "__main__":
    from textual.app import App

    class ColorInputsApp(App):
        CSS = """
        Screen {
            align: center middle;
        }
        """

        def compose(self) -> ComposeResult:
            yield ColorInputs()

    app = ColorInputsApp()
    app.run()
