from __future__ import annotations

from rich.segment import Segment
from rich.style import Style
from textual import events
from textual.color import BLACK, WHITE, Gradient
from textual.geometry import clamp
from textual.message import Message
from textual.reactive import reactive
from textual.strip import Strip
from textual.widget import Widget

_GRADIENT_COLORS = [
    "#ff0000",
    "#ffff00",
    "#00ff00",
    "#00ffff",
    "#0000ff",
    "#ff00ff",
    "#ff0000",
]


class HuePicker(Widget):
    DEFAULT_CSS = """
    HuePicker {
        height: 2;
    }
    """

    _GRADIENT = Gradient.from_colors(*_GRADIENT_COLORS)

    value: reactive[float] = reactive(0.0, init=False)
    """Hue value in the range 0 to 1."""

    class Changed(Message):
        """Posted when the hue value changes.

        This message can be handled using an `on_hue_picker_changed` method.
        """

        def __init__(self, hue_picker: HuePicker, value: float) -> None:
            super().__init__()
            self.value: float = value
            self.hue_picker: HuePicker = hue_picker

        @property
        def control(self) -> HuePicker:
            return self.hue_picker

    def __init__(
        self,
        value: float = 0.0,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.value = value
        """Create a hue picker widget.

        Args:
            value: The initial hue value in the range 0-1.
            name: The name of the widget.
            id: The ID of the widget in the DOM.
            classes: The CSS classes of the widget.
            disabled: Whether the widget is disabled or not.
        """

    def render_line(self, y: int) -> Strip:
        width = self.content_size.width

        get_color = self._GRADIENT.get_rich_color
        from_color = Style.from_color

        arrow_x = int(self.value * (width - 1))
        arrow_icon, arrow_color = ("▼", BLACK) if y == 0 else ("▲", WHITE)

        segments = [
            (
                Segment(
                    arrow_icon if x == arrow_x else " ",
                    from_color(
                        arrow_color.rich_color,
                        get_color(x / (width - 1)),
                    ),
                )
            )
            for x in range(width)
        ]

        return Strip(segments)

    def validate_value(self, value: float) -> float:
        return clamp(value, 0.0, 1.0)

    def watch_value(self) -> None:
        self.post_message(self.Changed(self, self.value))

    async def _on_mouse_down(self, event: events.MouseDown) -> None:
        mouse_x_norm = event.x / (self.content_size.width - 1)
        self.value = mouse_x_norm


if __name__ == "__main__":
    from textual.app import App, ComposeResult

    class HuePickerApp(App):
        CSS = """
        Screen {
            align: center middle;
        }

        HuePicker {
            width: 80%;
        }
        """

        def compose(self) -> ComposeResult:
            yield HuePicker()

    app = HuePickerApp()
    app.run()
