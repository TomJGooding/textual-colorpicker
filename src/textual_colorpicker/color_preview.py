from textual.app import RenderResult
from textual.color import Color
from textual.reactive import reactive
from textual.renderables.blank import Blank
from textual.widget import Widget


class ColorPreview(Widget):
    color: reactive[Color] = reactive(Color(255, 0, 0))
    """Color to display in the preview."""

    def __init__(
        self,
        color: Color = Color(255, 0, 0),
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        """Create a color preview widget.

        Args:
            color: Color to display in the preview.
            name: The name of the widget.
            id: The ID of the widget in the DOM.
            classes: The CSS classes of the widget.
            disabled: Whether the widget is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.color = color

    def render(self) -> RenderResult:
        return Blank(self.color)
