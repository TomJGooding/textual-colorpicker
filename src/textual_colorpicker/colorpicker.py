from typing import ClassVar

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.color import Color
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.validation import Integer
from textual.widget import Widget
from textual.widgets import Input, Label, Static


class RgbInput(Input):
    DEFAULT_CSS = """
    RgbInput {
        width: 10;
    }
    """

    def __init__(
        self,
        value: str | None = None,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            value,
            validators=[Integer(minimum=0, maximum=255)],
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )


class RgbTuner(Widget):
    DEFAULT_CSS = """
    RgbTuner {
        height: auto;
        width: auto;
    }

    RgbTuner Horizontal {
        height: auto;
        width: auto;
    }

    RgbTuner Label {
        padding: 1;
        text-style: underline;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("R")
            yield RgbInput(str(0), id="red", classes="input")
        with Horizontal():
            yield Label("G")
            yield RgbInput(str(0), id="green", classes="input")
        with Horizontal():
            yield Label("B")
            yield RgbInput(str(0), id="blue", classes="input")


class ColorPicker(Widget, can_focus=True):
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("r", "focus_red", "Red", show=False),
        Binding("g", "focus_green", "Green", show=False),
        Binding("b", "focus_blue", "Blue", show=False),
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
    color = reactive(Color(r=0, g=0, b=0))

    def compose(self) -> ComposeResult:
        yield RgbTuner()
        yield Static(id="color-preview")

    def compute_color(self) -> Color:
        return Color(self.red, self.green, self.blue).clamped

    def watch_color(self, color: Color) -> None:
        self.query_one("#color-preview").styles.background = color

    @on(RgbInput.Changed)
    def on_rgb_input_changed(self, event: RgbInput.Changed) -> None:
        assert event.validation_result is not None
        if not event.validation_result.is_valid:
            return

        if event.input.id == "red":
            self.red = int(event.value)
        elif event.input.id == "green":
            self.green = int(event.value)
        elif event.input.id == "blue":
            self.blue = int(event.value)

    def action_focus_red(self) -> None:
        self.query_one("#red", Input).focus()

    def action_focus_green(self) -> None:
        self.query_one("#green", Input).focus()

    def action_focus_blue(self) -> None:
        self.query_one("#blue", Input).focus()
