from __future__ import annotations

from textual.app import ComposeResult
from textual.color import HSV, Color
from textual.containers import VerticalGroup
from textual.message import Message
from textual.reactive import var
from textual.widget import Widget

from textual_colorpicker.color_inputs import ColorInputs, HexInput, HsvInputs, RgbInputs
from textual_colorpicker.color_preview import ColorPreview
from textual_colorpicker.hue_picker import HuePicker
from textual_colorpicker.saturation_value_picker import SaturationValuePicker


class ColorPicker(Widget):
    """A color picker widget."""

    DEFAULT_CSS = """
    ColorPicker {
        width: auto;
        height: auto;
        layout: horizontal;

        VerticalGroup {
            width: auto;
        }

        SaturationValuePicker {
            height: 17;
        }

        HuePicker {
            width: 37;
            margin-top: 1;
        }

        ColorPreview {
            height: 6;
            margin-bottom: 1;
            margin-left: 2;
        }

        ColorInputs {
            margin-left: 2;
        }
    }
    """

    color: var[Color] = var(Color(255, 0, 0), init=False)
    """The current color value."""

    _hsv: var[HSV] = var(HSV(0.0, 1.0, 1.0), init=False)
    """The current HSV color value."""

    class Changed(Message):
        """Posted when the color value changes.

        This message can be handled using an `on_color_picker_changed` method.
        """

        def __init__(self, color_picker: ColorPicker, color: Color) -> None:
            super().__init__()
            self.color: Color = color
            self.color_picker = color_picker

        @property
        def control(self) -> ColorPicker:
            return self.color_picker

    def __init__(
        self,
        color: Color = Color(255, 0, 0),
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Create a color picker widget.

        Args:
            color: The initial color value.
            name: The name of the widget.
            id: The ID of the widget in the DOM.
            classes: The CSS classes of the widget.
            disabled: Whether the widget is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        color = color.clamped
        self.color = color
        self._hsv = color.hsv

    def compose(self) -> ComposeResult:
        hsv = self._hsv
        with VerticalGroup():
            yield SaturationValuePicker(hsv)
            yield HuePicker(hsv.h)
        with VerticalGroup():
            yield ColorPreview(self.color)
            yield ColorInputs(self.color)

    def validate_color(self, color: Color) -> Color:
        return color.clamped

    def watch_color(self) -> None:
        hsv = self.color.hsv
        self.set_reactive(ColorPicker._hsv, hsv)

        self._update_all_from_color_and_hsv()

        self.post_message(self.Changed(self, self.color))

    def _watch__hsv(self) -> None:
        old_color = self.color
        new_color = Color.from_hsv(*self._hsv)
        self.set_reactive(ColorPicker.color, new_color)

        self._update_all_from_color_and_hsv()

        if new_color != old_color:
            self.post_message(self.Changed(self, self.color))

    def _update_all_from_color_and_hsv(self) -> None:
        if not self.is_mounted:
            return
        color = self.color
        self.query_one(ColorPreview).color = color
        self.query_one(RgbInputs).color = color
        self.query_one(HexInput).value = color.hex

        hsv = self._hsv
        self.query_one(HuePicker).hue = hsv.h
        self.query_one(SaturationValuePicker).hsv = hsv
        self.query_one(HsvInputs).hsv = hsv

    def _on_hue_picker_changed(self, event: HuePicker.Changed) -> None:
        event.stop()
        h = event.hue
        _, s, v = self._hsv
        self._hsv = HSV(h, s, v)

    def _on_saturation_value_picker_changed(
        self, event: SaturationValuePicker.Changed
    ) -> None:
        event.stop()
        h, _, _ = self._hsv
        _, s, v = event.hsv
        self._hsv = HSV(h, s, v)

    def _on_rgb_inputs_changed(self, event: RgbInputs.Changed) -> None:
        event.stop()
        self.color = event.color

    def _on_hsv_inputs_changed(self, event: HsvInputs.Changed) -> None:
        event.stop()
        self._hsv = event.hsv

    def _on_hex_input_changed(self, event: HexInput.Changed) -> None:
        event.stop()
        color = Color.parse(event.value)
        self.color = color


if __name__ == "__main__":
    from textual.app import App

    class ColorPickerApp(App):
        CSS = """
        Screen {
            align: center middle;
        }
        """

        def compose(self) -> ComposeResult:
            yield ColorPicker()

    app = ColorPickerApp()
    app.run()
