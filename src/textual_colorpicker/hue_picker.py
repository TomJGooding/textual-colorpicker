from rich.color import Color as RichColor
from rich.segment import Segment
from rich.style import Style
from textual import events
from textual.color import Gradient
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

    _GRADIENT = Gradient(
        *[
            (i / (len(_GRADIENT_COLORS) - 1), color)
            for i, color in enumerate(_GRADIENT_COLORS)
        ]
    )

    _slider_position: reactive[float] = reactive(0.0)

    def render_line(self, y: int) -> Strip:
        width = self.content_size.width

        get_color = self._GRADIENT.get_rich_color
        from_color = Style.from_color

        black = RichColor.from_rgb(0, 0, 0)
        white = RichColor.from_rgb(255, 255, 255)

        arrow_x = int(self._slider_position * (width - 1))
        arrow_icon, arrow_color = ("▼", black) if y == 0 else ("▲", white)

        segments = [
            (
                Segment(
                    arrow_icon if x == arrow_x else " ",
                    from_color(
                        arrow_color,
                        get_color(x / (width - 1)),
                    ),
                )
            )
            for x in range(width)
        ]

        return Strip(segments)

    async def _on_click(self, event: events.Click) -> None:
        mouse_x_norm = event.x / (self.content_size.width - 1)
        self._slider_position = mouse_x_norm
