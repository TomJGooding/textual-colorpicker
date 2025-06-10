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
    ALLOW_SELECT = False

    DEFAULT_CSS = """
    HuePicker {
        height: 2;
    }
    """

    _GRADIENT = Gradient.from_colors(*_GRADIENT_COLORS)

    hue: reactive[float] = reactive(0.0, init=False)
    """The currently selected hue value in the range 0 to 1."""

    class Changed(Message):
        """Posted when the hue value changes.

        This message can be handled using an `on_hue_picker_changed` method.
        """

        def __init__(self, hue_picker: HuePicker, hue: float) -> None:
            super().__init__()
            self.hue: float = hue
            self.hue_picker: HuePicker = hue_picker

        @property
        def control(self) -> HuePicker:
            return self.hue_picker

    def __init__(
        self,
        hue: float = 0.0,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Create a hue picker widget.

        Args:
            hue: The initial hue value in the range 0 to 1.
            name: The name of the widget.
            id: The ID of the widget in the DOM.
            classes: The CSS classes of the widget.
            disabled: Whether the widget is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.hue = hue
        self._grabbed = False

    def render_line(self, y: int) -> Strip:
        width = self.content_size.width

        get_color = self._GRADIENT.get_rich_color
        from_color = Style.from_color

        arrow_x = int(self.hue * (width - 1) + 0.5)
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

    def validate_hue(self, hue: float) -> float:
        return clamp(hue, 0.0, 1.0)

    def watch_hue(self) -> None:
        self.post_message(self.Changed(self, self.hue))

    async def _on_mouse_down(self, event: events.MouseDown) -> None:
        mouse_offset = event.get_content_offset(self)
        if mouse_offset is None:
            return
        mouse_x_norm = mouse_offset.x / (self.content_size.width - 1)
        self.hue = mouse_x_norm

    # TODO: Enable click and drag for the hue picker. Unfortunately this causes
    # the app to lag and eventually freeze entirely when implemented in the
    # color picker widget.
    #
    #     self._grabbed = True
    #     self.capture_mouse(True)
    #
    # async def _on_mouse_move(self, event: events.MouseMove) -> None:
    #     mouse_offset = event.get_content_offset(self)
    #     if self._grabbed and mouse_offset is not None:
    #         mouse_x_norm = mouse_offset.x / (self.content_size.width - 1)
    #         self.hue = mouse_x_norm
    #
    # async def _on_mouse_up(self, event: events.MouseUp) -> None:
    #     if self._grabbed:
    #         self._grabbed = False
    #         self.release_mouse()


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
