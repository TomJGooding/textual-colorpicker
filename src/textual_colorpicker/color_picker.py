from textual.app import ComposeResult
from textual.color import HSV
from textual.containers import VerticalGroup
from textual.reactive import var
from textual.widget import Widget

from textual_colorpicker._color_hsv import _color_from_hsv
from textual_colorpicker.color_inputs import ColorInputs, HexInput, HSVInputs, RGBInputs
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
            width: 36;
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

    _hsv = var(HSV(0.0, 1.0, 1.0), init=False)

    def compose(self) -> ComposeResult:
        hsv = self._hsv
        color = _color_from_hsv(*hsv)
        with VerticalGroup():
            yield SaturationValuePicker(hsv)
            yield HuePicker(hsv.h)
        with VerticalGroup():
            yield ColorPreview(color)
            yield ColorInputs(disabled=True)

    def _watch__hsv(self, hsv: HSV) -> None:
        color = _color_from_hsv(*hsv)

        self.query_one(SaturationValuePicker).hsv = hsv
        self.query_one(HuePicker).value = hsv.h

        self.query_one(ColorPreview).color = color

        self.query_one(HSVInputs).hsv = hsv
        self.query_one(RGBInputs).color = color
        self.query_one(HexInput).value = color.hex.lstrip("#")

    def _on_saturation_value_picker_changed(
        self, event: SaturationValuePicker.Changed
    ) -> None:
        event.stop()
        h = self._hsv.h
        _, s, v = event.hsv
        with self.prevent(SaturationValuePicker.Changed):
            self._hsv = HSV(h, s, v)

    def _on_hue_picker_changed(self, event: HuePicker.Changed) -> None:
        event.stop()
        h = event.value
        _, s, v = self._hsv
        with self.prevent(HuePicker.Changed):
            self._hsv = HSV(h, s, v)


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
