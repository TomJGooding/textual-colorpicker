from __future__ import annotations

import re

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


class RgbInputs(Widget):
    """An RGB inputs widget that combines fields for Red, Green and Blue values."""

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
    """The current color value."""

    class Changed(Message):
        """Posted when the color value changes.

        This message can be handled using an `on_rgb_inputs_changed` method.
        """

        def __init__(self, rgb_inputs: RgbInputs, color: Color) -> None:
            super().__init__()
            self.color: Color = color
            self.rgb_inputs: RgbInputs = rgb_inputs

        @property
        def control(self) -> RgbInputs:
            return self.rgb_inputs

    def __init__(
        self,
        color: Color = Color(255, 0, 0),
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Create an RGB inputs widget.

        Args:
            color: The initial color value.
            name: The name of the widget.
            id: The ID of the widget in the DOM.
            classes: The CSS classes of the widget.
            disabled: Whether the widget is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.color = color

    def compose(self) -> ComposeResult:
        r, g, b = self.color.rgb
        with HorizontalGroup():
            yield Label("R:")
            yield Input(
                str(r),
                validators=Integer(0, 255),
                classes="--red-input",
            )
        with HorizontalGroup():
            yield Label("G:")
            yield Input(
                str(g),
                validators=Integer(0, 255),
                classes="--green-input",
            )
        with HorizontalGroup():
            yield Label("B:")
            yield Input(
                str(b),
                validators=Integer(0, 255),
                classes="--blue-input",
            )

    def validate_color(self, color: Color) -> Color:
        return color.clamped

    def watch_color(self) -> None:
        self._update_all_from_color()

        self.post_message(self.Changed(self, self.color))

    def _update_all_from_color(self) -> None:
        if not self.is_mounted:
            return
        red_input = self.query_one(".--red-input", Input)
        green_input = self.query_one(".--green-input", Input)
        blue_input = self.query_one(".--blue-input", Input)

        r, g, b = self.color.rgb

        red_input.value = str(r)
        green_input.value = str(g)
        blue_input.value = str(b)

    @on(Input.Blurred)
    @on(Input.Submitted)
    def _on_input_blurred_or_submitted(
        self, event: Input.Blurred | Input.Submitted
    ) -> None:
        event.stop()
        validation_result = event.validation_result
        assert validation_result is not None
        if not validation_result.is_valid:
            failure = validation_result.failures[0]
            # If the value is not a number, set the input to zero.
            if isinstance(failure, Integer.NotANumber):
                event.input.value = str(0)
            # If the value is not in range, set the input to the clamped value.
            # NOTE: The value may also be a float, so we convert it as necessary.
            elif isinstance(failure, Integer.NotInRange):
                clamped_value = clamp(float(event.value), 0, 255)
                event.input.value = str(int(clamped_value))
            # If the value is a float, round to the nearest integer.
            elif isinstance(failure, Integer.NotAnInteger):
                rounded_value = int(float(event.value) + 0.5)
                event.input.value = str(rounded_value)

        r = int(self.query_one(".--red-input", Input).value)
        g = int(self.query_one(".--green-input", Input).value)
        b = int(self.query_one(".--blue-input", Input).value)
        color = Color(r, g, b)

        self.color = color

    @on(Input.Changed)
    def _on_input_changed(self, event: Input.Changed) -> None:
        event.stop()


class HsvInputs(Widget):
    """An HSV inputs widget that combines fields for Hue, Saturation and Value values."""

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
    """The current HSV (Hue, Saturation, Value) values in the range 0 to 1."""

    class Changed(Message):
        """Posted when the HSV (Hue, Saturation, Value) value changes.

        This message can be handled using an `on_hsv_inputs_changed` method.
        """

        def __init__(self, hsv_inputs: HsvInputs, hsv: HSV) -> None:
            super().__init__()
            self.hsv: HSV = hsv
            self.hsv_inputs: HsvInputs = hsv_inputs

        @property
        def control(self) -> HsvInputs:
            return self.hsv_inputs

    def __init__(
        self,
        hsv: HSV = HSV(0.0, 1.0, 1.0),
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Create an HSV inputs widget.

        Args:
            hsv: The initial HSV (Hue, Saturation, Value) values in the range 0 to 1.
            name: The name of the widget.
            id: The ID of the widget in the DOM.
            classes: The CSS classes of the widget.
            disabled: Whether the widget is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.hsv = hsv

    def compose(self) -> ComposeResult:
        h, s, v = self._hsv_scaled_integers(self.hsv)
        with HorizontalGroup():
            yield Label("H:")
            yield Input(
                str(h),
                validators=Integer(0, 360),
                classes="--hue-input",
            )
        with HorizontalGroup():
            yield Label("S:")
            yield Input(
                str(s),
                validators=Integer(0, 100),
                classes="--saturation-input",
            )
        with HorizontalGroup():
            yield Label("V:")
            yield Input(
                str(v),
                validators=Integer(0, 100),
                classes="--value-input",
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
        self._update_all_from_hsv()

        self.post_message(self.Changed(self, self.hsv))

    def _hsv_scaled_integers(self, hsv: HSV) -> tuple[int, int, int]:
        h = int(hsv.h * 360 + 0.5)
        s = int(hsv.s * 100 + 0.5)
        v = int(hsv.v * 100 + 0.5)

        return h, s, v

    def _update_all_from_hsv(self) -> None:
        if not self.is_mounted:
            return
        hue_input = self.query_one(".--hue-input", Input)
        saturation_input = self.query_one(".--saturation-input", Input)
        value_input = self.query_one(".--value-input", Input)

        h, s, v = self._hsv_scaled_integers(self.hsv)

        hue_input.value = str(h)
        saturation_input.value = str(s)
        value_input.value = str(v)

    @on(Input.Blurred)
    @on(Input.Submitted)
    def _on_input_blurred_or_submitted(
        self, event: Input.Blurred | Input.Submitted
    ) -> None:
        event.stop()
        validation_result = event.validation_result
        assert validation_result is not None
        if not validation_result.is_valid:
            failure = validation_result.failures[0]
            # If the value is not a number, set the input to zero.
            if isinstance(failure, Integer.NotANumber):
                event.input.value = str(0)
            # If the value is not in range, set the input to the clamped value.
            # NOTE: The value may also be a float, so we convert it as necessary.
            elif isinstance(failure, Integer.NotInRange):
                max = 360 if event.input.has_class(".--hue-input") else 100
                clamped_value = clamp(float(event.value), 0, max)
                event.input.value = str(int(clamped_value))
            # If the value is a float, round to the nearest integer.
            elif isinstance(failure, Integer.NotAnInteger):
                rounded_value = int(float(event.value) + 0.5)
                event.input.value = str(rounded_value)

        h = int(self.query_one(".--hue-input", Input).value)
        s = int(self.query_one(".--saturation-input", Input).value)
        v = int(self.query_one(".--value-input", Input).value)
        hsv = HSV(h / 360, s / 100, v / 100)

        self.hsv = hsv

    @on(Input.Changed)
    def _on_input_changed(self, event: Input.Changed) -> None:
        event.stop()


class HexInput(Widget):
    """A hex color input widget."""

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
    _HEX_COLOR_PATTERN = r"#[0-9a-fA-F]{6}"

    value: var[str] = var("#FF0000", init=False)
    """The current hex color value."""

    class Changed(Message):
        """Posted when the hex color value changes.

        This message can be handled using an `on_hex_input_changed` method.
        """

        def __init__(self, hex_input: HexInput, value: str) -> None:
            super().__init__()
            self.value: str = value
            self.hex_input = hex_input

        @property
        def control(self) -> HexInput:
            return self.hex_input

    def __init__(
        self,
        value: str = "#FF0000",
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Create a hex color input widget.

        Args:
            value: The initial hex color value.
            name: The name of the widget.
            id: The ID of the widget in the DOM.
            classes: The CSS classes of the widget.
            disabled: Whether the widget is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.value = value.upper()

    def compose(self) -> ComposeResult:
        hex_value = self._format_hex_value(self.value)
        with HorizontalGroup():
            yield Label("#")
            yield Input(
                hex_value,
                validators=Regex(self._HEX_COLOR_PATTERN[1:]),
            )

    def validate_value(self, value: str) -> str:
        if re.fullmatch(self._HEX_COLOR_PATTERN, value):
            return value.upper()
        raise ValueError(f"Invalid hex color: {value}")

    def watch_value(self) -> None:
        if self.is_mounted:
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
            # If the value is not a valid hex color, reset the input to the
            # current hex value.
            if not re.fullmatch(self._HEX_COLOR_PATTERN, event.value):
                hex_value = self._format_hex_value(self.value)
                event.input.value = hex_value
                return

        # If the value is a valid hex color but starts with the "#" prefix,
        # simply strip the "#" from the input.
        hex_value = self._format_hex_value(event.value)
        event.input.value = hex_value

        hex_color = f"#{hex_value.upper()}"
        self.value = hex_color

    @on(Input.Changed)
    def _on_input_changed(self, event: Input.Changed) -> None:
        event.stop()


class ColorInputs(Widget):
    """A color inputs widget that combines fields for RGB, HSV and Hex values."""

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
    """The current color value."""

    class Changed(Message):
        """Posted when the color value changes.

        This message can be handled using an `on_color_inputs_changed` method.
        """

        def __init__(self, color_inputs: ColorInputs, color: Color) -> None:
            super().__init__()
            self.color: Color = color
            self.color_inputs: ColorInputs = color_inputs

        @property
        def control(self) -> ColorInputs:
            return self.color_inputs

    def __init__(
        self,
        color: Color = Color(255, 0, 0),
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Create a color inputs widget.

        Args:
            color: The initial color value.
            name: The name of the widget.
            id: The ID of the widget in the DOM.
            classes: The CSS classes of the widget.
            disabled: Whether the widget is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.color = color

    def compose(self) -> ComposeResult:
        h, s, v = self.color.hsv
        hex = self.color.hex
        with HorizontalGroup():
            yield RgbInputs(self.color)
            yield HsvInputs(HSV(h, s, v))
        yield HexInput(hex)

    def validate_color(self, color: Color) -> Color:
        return color.clamped

    def watch_color(self) -> None:
        self._update_all_from_color()

        self.post_message(self.Changed(self, self.color))

    def _update_all_from_color(self) -> None:
        if not self.is_mounted:
            return
        color = self.color
        h, s, v = color.hsv
        hex = color.hex
        self.query_one(RgbInputs).color = color
        self.query_one(HsvInputs).hsv = HSV(h, s, v)
        self.query_one(HexInput).value = hex

    def _on_rgb_inputs_changed(self, event: RgbInputs.Changed) -> None:
        event.stop()
        self.color = event.color

    def _on_hsv_inputs_changed(self, event: HsvInputs.Changed) -> None:
        event.stop()
        color = Color.from_hsv(*event.hsv)
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
