from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Input, Static


class ColorPicker(Widget, can_focus=True):
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("r", "focus_red", "Red", show=False),
        Binding("g", "focus_green", "Green", show=False),
        Binding("b", "focus_blue", "Blue", show=False),
        Binding("a", "focus_alpha", "Alpha", show=False),
    ]

    DEFAULT_CSS = """
    ColorPicker > #form {
        height: auto;
        layout: grid;
        grid-size: 2 4;
        grid-rows: 4;
        grid-columns: 3 10;
    }

    ColorPicker .label {
        padding: 1 1;
        text-align: right;
        text-style: underline;
    }
    """

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

    def compose(self) -> ComposeResult:
        with Container(id="form"):
            yield Static("R", classes="label")
            yield Input("0", id="red", classes="input")
            yield Static("G", classes="label")
            yield Input("0", id="green", classes="input")
            yield Static("B", classes="label")
            yield Input("0", id="blue", classes="input")
            yield Static("A", classes="label")
            yield Input("0", id="alpha", classes="input")

    def action_focus_red(self) -> None:
        self.query_one("#red", Input).focus()

    def action_focus_green(self) -> None:
        self.query_one("#green", Input).focus()

    def action_focus_blue(self) -> None:
        self.query_one("#blue", Input).focus()

    def action_focus_alpha(self) -> None:
        self.query_one("#alpha", Input).focus()
