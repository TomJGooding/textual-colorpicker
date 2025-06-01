from __future__ import annotations

from textual.app import ComposeResult
from textual.color import HSV, Color
from textual.containers import VerticalGroup
from textual.reactive import var
from textual.widget import Widget

from textual_colorpicker.color_inputs import ColorInputs
from textual_colorpicker.color_preview import ColorPreview
from textual_colorpicker.hue_picker import HuePicker
from textual_colorpicker.saturation_value_picker import SaturationValuePicker


class ColorPicker(Widget):
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

    def __init__(
        self,
        color: Color = Color(255, 0, 0),
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.color = color

    def compose(self) -> ComposeResult:
        h, s, v = self.color.hsv
        with VerticalGroup():
            yield SaturationValuePicker(HSV(h, s, v))
            yield HuePicker(h)
        with VerticalGroup():
            yield ColorPreview(self.color)
            yield ColorInputs(self.color)

    def validate_color(self, color: Color) -> Color:
        return color.clamped

    def watch_color(self) -> None:
        self._update_all_from_color(self.color)

    def _update_all_from_color(self, color: Color) -> None:
        if not self.is_mounted:
            return
        self.query_one(ColorPreview).color = color
        self.query_one(ColorInputs).color = color

        h, s, v = color.hsv
        self.query_one(HuePicker).hue = h
        self.query_one(SaturationValuePicker).hsv = HSV(h, s, v)

    def _on_color_inputs_changed(self, event: ColorInputs.Changed) -> None:
        event.stop()
        self.color = event.color

    def _on_hue_picker_changed(self, event: HuePicker.Changed) -> None:
        event.stop()
        h = event.hue
        _, s, v = self.color.hsv
        color = Color.from_hsv(h, s, v)
        self.color = color

    def _on_saturation_value_picker_changed(
        self, event: SaturationValuePicker.Changed
    ) -> None:
        event.stop()
        h, _, _ = self.color.hsv
        _, s, v = event.hsv
        color = Color.from_hsv(h, s, v)
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
