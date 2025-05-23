from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.color import HSV, Color
from textual.containers import HorizontalGroup
from textual.geometry import clamp
from textual.message import Message
from textual.reactive import var
from textual.validation import Integer, Regex
from textual.widget import Widget
from textual.widgets import Input, Label

from textual_colorpicker._color_hsv import _color_from_hsv, _hsv_from_color


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

    class Changed(Message):
        def __init__(self, hsv_inputs: HsvInputs, hsv: HSV) -> None:
            super().__init__()
            self.hsv: HSV = hsv
            self.hsv_inputs: HsvInputs = hsv_inputs

        @property
        def control(self) -> HsvInputs:
            return self.hsv_inputs

    def compose(self) -> ComposeResult:
        h, s, v = self._hsv_scaled_values(self.hsv)
        with HorizontalGroup():
            yield Label("H:")
            yield Input(
                str(h),
                validators=Integer(0, 360),
                id="--hue-input",
            )
        with HorizontalGroup():
            yield Label("S:")
            yield Input(
                str(s),
                validators=Integer(0, 100),
                id="--saturation-input",
            )
        with HorizontalGroup():
            yield Label("V:")
            yield Input(
                str(v),
                validators=Integer(0, 100),
                id="--value-input",
            )

    def validate_hsv(self, hsv: HSV) -> HSV:
        h, s, v = hsv
        clamped_hsv = HSV(
            clamp(h, 0.0, 1.0),
            clamp(s, 0.0, 1.0),
            clamp(v, 0.0, 1.0),
        )

        return clamped_hsv

    def watch_hsv(self) -> None:
        self._update_all_from_hsv(self.hsv)

        self.post_message(self.Changed(self, self.hsv))

    def _hsv_scaled_values(self, hsv: HSV) -> tuple[int, int, int]:
        h = int(hsv.h * 360 + 0.5)
        s = int(hsv.s * 100 + 0.5)
        v = int(hsv.v * 100 + 0.5)

        return h, s, v

    def _update_all_from_hsv(self, hsv: HSV) -> None:
        hue_input = self.query_one("#--hue-input", Input)
        saturation_input = self.query_one("#--saturation-input", Input)
        value_input = self.query_one("#--value-input", Input)

        h, s, v = self._hsv_scaled_values(hsv)

        hue_input.value = str(h)
        saturation_input.value = str(s)
        value_input.value = str(v)

        # Force a re-validation of the input selections.
        # Workaround for https://github.com/Textualize/textual/issues/5811
        hue_input.selection = hue_input.selection
        saturation_input.selection = saturation_input.selection
        value_input.selection = value_input.selection

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
        h = int(float(self.query_one("#--hue-input", Input).value) + 0.5)
        s = int(float(self.query_one("#--saturation-input", Input).value) + 0.5)
        v = int(float(self.query_one("#--value-input", Input).value) + 0.5)

        clamped_hsv = HSV(
            clamp(h / 360, 0.0, 1.0),
            clamp(s / 100, 0.0, 1.0),
            clamp(v / 100, 0.0, 1.0),
        )
        # If the value is not in range, set the input to the clamped value.
        self._update_all_from_hsv(clamped_hsv)

        self.hsv = clamped_hsv


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

    # TODO: Allow shorthand hex values
    _HEX_VALUE_PATTERN = r"[0-9a-fA-F]{6}"

    value: var[str] = var("#FF0000", init=False)

    class Changed(Message):
        def __init__(self, hex_input: HexInput, value: str) -> None:
            super().__init__()
            self.value: str = value
            self.hex_input = hex_input

        @property
        def control(self) -> HexInput:
            return self.hex_input

    def compose(self) -> ComposeResult:
        hex_value = self._format_hex_value(self.value)
        with HorizontalGroup():
            yield Label("#")
            yield Input(
                hex_value,
                validators=Regex(self._HEX_VALUE_PATTERN),
            )

    def watch_value(self) -> None:
        hex_value = self._format_hex_value(self.value)
        self.query_one(Input).value = hex_value

        self.post_message(self.Changed(self, self.value))

    def _format_hex_value(self, hex: str) -> str:
        return hex.lower().lstrip("#")

    @on(Input.Blurred)
    @on(Input.Submitted)
    def _on_input_blurred_or_submitted(
        self, event: Input.Blurred | Input.Submitted
    ) -> None:
        event.stop()
        validation_result = event.validation_result
        assert validation_result is not None
        if not validation_result.is_valid:
            # TODO: If the value is a valid hex but starts with the "#" prefix,
            # simply strip the "#" from the input.
            hex_value = self._format_hex_value(self.value)
            event.input.value = hex_value
            # Force a re-validation of the input selection.
            # Workaround for https://github.com/Textualize/textual/issues/5811
            event.input.selection = event.input.selection
            return

        hex = f"#{event.value.upper()}"
        self.value = hex


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
            yield HsvInputs()
        yield HexInput()

    def watch_color(self) -> None:
        h, s, v = _hsv_from_color(self.color)
        hex = self.color.hex
        self.query_one(RgbInputs).color = self.color
        self.query_one(HsvInputs).hsv = HSV(h, s, v)
        self.query_one(HexInput).value = hex

    def _on_rgb_inputs_changed(self, event: RgbInputs.Changed) -> None:
        event.stop()
        self.color = event.color

    def _on_hsv_inputs_changed(self, event: HsvInputs.Changed) -> None:
        event.stop()
        color = _color_from_hsv(*event.hsv)
        self.color = color

    def _on_hex_input_changed(self, event: HexInput.Changed) -> None:
        event.stop()
        color = Color.parse(event.value)
        self.color = color


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
