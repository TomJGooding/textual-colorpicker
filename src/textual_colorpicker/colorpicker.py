from typing import ClassVar

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.color import Color
from textual.containers import Container
from textual.reactive import reactive
from textual.validation import Integer
from textual.widget import Widget
from textual.widgets import Input, Static


class RgbInput(Input):
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

    class RgbForm(Container):
        DEFAULT_CSS = """
        RgbForm {
            height: auto;
            layout: grid;
            grid-size: 2 3;
            grid-rows: 4;
            grid-columns: 3 10;
        }

        RgbForm .label {
            padding: 1 1;
            text-align: right;
            text-style: underline;
        }
        """

        def compose(self) -> ComposeResult:
            yield Static("R", classes="label")
            yield RgbInput(str(0), id="red", classes="input")
            yield Static("G", classes="label")
            yield RgbInput(str(0), id="green", classes="input")
            yield Static("B", classes="label")
            yield RgbInput(str(0), id="blue", classes="input")

    def compose(self) -> ComposeResult:
        yield self.RgbForm()
        yield Static(id="color-preview")

    def compute_color(self) -> Color:
        return Color(self.red, self.green, self.blue).clamped

    def watch_color(self, color: Color) -> None:
        self.query_one("#color-preview").styles.background = color

    @on(RgbInput.Changed, "#red")
    def on_red_input_changed(self, event: RgbInput.Changed) -> None:
        assert event.validation_result is not None
        if event.validation_result.is_valid:
            self.red = int(event.value)

    @on(RgbInput.Changed, "#green")
    def on_green_input_changed(self, event: RgbInput.Changed) -> None:
        assert event.validation_result is not None
        if event.validation_result.is_valid:
            self.green = int(event.value)

    @on(RgbInput.Changed, "#blue")
    def on_blue_input_changed(self, event: RgbInput.Changed) -> None:
        assert event.validation_result is not None
        if event.validation_result.is_valid:
            self.blue = int(event.value)

    def action_focus_red(self) -> None:
        self.query_one("#red", Input).focus()

    def action_focus_green(self) -> None:
        self.query_one("#green", Input).focus()

    def action_focus_blue(self) -> None:
        self.query_one("#blue", Input).focus()
