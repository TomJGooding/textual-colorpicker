from typing import ClassVar

from rich.highlighter import Highlighter
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.color import Color
from textual.containers import Container
from textual.reactive import reactive
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
    ColorPicker > #color-preview {
        height: 10;
        width: 20;
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

    red = reactive(0)
    green = reactive(0)
    blue = reactive(0)
    alpha = reactive(1.0)
    color = reactive(Color(r=0, g=0, b=0, a=1.0))

    class RgbaForm(Container):
        DEFAULT_CSS = """
        RgbaForm {
            height: auto;
            layout: grid;
            grid-size: 2 4;
            grid-rows: 4;
            grid-columns: 3 10;
        }

        RgbaForm .label {
            padding: 1 1;
            text-align: right;
            text-style: underline;
        }
        """

        def compose(self) -> ComposeResult:
            yield Static("R", classes="label")
            yield IntegerInput(0, id="red", classes="input")
            yield Static("G", classes="label")
            yield IntegerInput(0, id="green", classes="input")
            yield Static("B", classes="label")
            yield IntegerInput(0, id="blue", classes="input")
            yield Static("A", classes="label")
            yield FloatInput(1.0, id="alpha", classes="input")

    def compose(self) -> ComposeResult:
        yield self.RgbaForm()
        yield Static(id="color-preview")

    def compute_color(self) -> Color:
        return Color(self.red, self.green, self.blue, self.alpha).clamped

    def watch_color(self, color: Color) -> None:
        self.query_one("#color-preview").styles.background = color

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "alpha":
            try:
                component = float(event.value)
            except ValueError:
                pass
            else:
                self.alpha = float(component)
        else:
            try:
                component = int(event.value)
            except ValueError:
                pass
            else:
                if event.input.id == "red":
                    self.red = int(component)
                elif event.input.id == "green":
                    self.green = int(component)
                elif event.input.id == "blue":
                    self.blue = int(component)

    def action_focus_red(self) -> None:
        self.query_one("#red", Input).focus()

    def action_focus_green(self) -> None:
        self.query_one("#green", Input).focus()

    def action_focus_blue(self) -> None:
        self.query_one("#blue", Input).focus()

    def action_focus_alpha(self) -> None:
        self.query_one("#alpha", Input).focus()


class IntegerInput(Input):
    def __init__(
        self,
        value: int | None = None,
        placeholder: str = "",
        highlighter: Highlighter | None = None,
        password: bool = False,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            value=str(value),
            placeholder=placeholder,
            highlighter=highlighter,
            password=password,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

    def insert_text_at_cursor(self, text: str) -> None:
        try:
            int(text)
        except ValueError:
            pass
        else:
            super().insert_text_at_cursor(text)


class FloatInput(Input):
    def __init__(
        self,
        value: float | None = None,
        placeholder: str = "",
        highlighter: Highlighter | None = None,
        password: bool = False,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            value=str(value),
            placeholder=placeholder,
            highlighter=highlighter,
            password=password,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

    def insert_text_at_cursor(self, text: str) -> None:
        if text == ".":
            if "." in self.value:
                pass
            else:
                super().insert_text_at_cursor(text)
        else:
            try:
                int(text)
            except ValueError:
                pass
            else:
                super().insert_text_at_cursor(text)
