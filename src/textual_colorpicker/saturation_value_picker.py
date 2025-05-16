from __future__ import annotations

from colorsys import hsv_to_rgb

from rich.segment import Segment
from rich.style import Style
from textual import events
from textual.color import HSV, WHITE, Color
from textual.geometry import clamp
from textual.message import Message
from textual.reactive import reactive
from textual.strip import Strip
from textual.widget import Widget


# NOTE: Currently Textual's `Color` class is missing HSV support.
# I've submitted a pull request to add a `Color.from_hsv` class method here:
# https://github.com/Textualize/textual/pull/5803
def _color_from_hsv(h: float, s: float, v: float) -> Color:
    r, g, b = hsv_to_rgb(h, s, v)
    return Color(int(r * 255 + 0.5), int(g * 255 + 0.5), int(b * 255 + 0.5))


class SaturationValuePicker(Widget):

    hsv = reactive(HSV(0.0, 1.0, 1.0), init=False)
    """The currently selected HSV (Hue, Saturation, Value) values"""

    class Changed(Message):
        """Posted when the HSV (Hue, Saturation, Value) value changes.

        This message can be handled using an `on_saturation_value_picker_changed` method.
        """

        def __init__(
            self, saturation_value_picker: SaturationValuePicker, hsv: HSV
        ) -> None:
            super().__init__()
            self.hsv: HSV = hsv
            self.satuation_value_picker: SaturationValuePicker = saturation_value_picker

        @property
        def control(self) -> SaturationValuePicker:
            return self.satuation_value_picker

    def __init__(
        self,
        hsv: HSV = HSV(0.0, 1.0, 1.0),
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.hsv = hsv
        """Create a two-dimensional saturation/value picker widget.

        Args:
            hsv: The initial HSV (Hue, Saturation, Value) values.
            name: The name of the widget.
            id: The ID of the widget in the DOM.
            classes: The CSS classes of the widget.
            disabled: Whether the widget is disabled or not.
        """

    def render_line(self, y: int) -> Strip:
        width = self.content_size.width
        height = self.content_size.height

        from_color = Style.from_color

        hue = self.hsv.h
        value = 1 - (y / (height - 1))

        pointer_y = int((1 - self.hsv.v) * (height - 1) + 0.5)
        pointer_x = int(self.hsv.s * (width - 1) + 0.5)

        segments: list[Segment] = []
        for x in range(width):
            saturation = x / (width - 1)
            style = from_color(
                WHITE.rich_color,
                _color_from_hsv(hue, saturation, value).rich_color,
            )

            if (y, x) == (pointer_y, pointer_x):
                char = "╬"
            elif y == pointer_y:
                char = "═"
            elif x == pointer_x:
                char = "║"
            else:
                char = " "

            segments.append(Segment(char, style))

        return Strip(segments)

    def validate_hsv(self, hsv: HSV) -> HSV:
        h, s, v = hsv

        clamped_hsv = HSV(
            clamp(h, 0.0, 1.0),
            clamp(s, 0.0, 1.0),
            clamp(v, 0.0, 1.0),
        )

        return clamped_hsv

    def watch_hsv(self) -> None:
        self.post_message(self.Changed(self, self.hsv))

    async def _on_click(self, event: events.Click) -> None:
        width = self.content_size.width
        height = self.content_size.height

        mouse_y_norm = event.y / (height - 1)
        mouse_x_norm = event.x / (width - 1)

        hue = self.hsv.h
        saturation = mouse_x_norm
        value = 1 - mouse_y_norm
        self.hsv = HSV(hue, saturation, value)


if __name__ == "__main__":
    from textual.app import App, ComposeResult

    class SaturationValuePickerApp(App):
        CSS = """
        Screen {
            align: center middle;
        }

        SaturationValuePicker {
            width: 80%;
            height: 80%;
        }
        """

        def compose(self) -> ComposeResult:
            yield SaturationValuePicker()

    app = SaturationValuePickerApp()
    app.run()
