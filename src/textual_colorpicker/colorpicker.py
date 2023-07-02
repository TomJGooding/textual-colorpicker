from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.color import Color
from textual.containers import Horizontal
from textual.message import Message
from textual.reactive import var
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

    red = var(0)
    green = var(0)
    blue = var(0)
    value = var(Color(r=0, g=0, b=0))

    class Changed(Message):
        def __init__(self, rgb_tuner: RgbTuner, value: Color) -> None:
            super().__init__()
            self.value: Color = value
            self.rgb_tuner: RgbTuner = rgb_tuner

        @property
        def control(self) -> RgbTuner:
            return self.rgb_tuner

    def watch_value(self, value: Color) -> None:
        self.post_message(self.Changed(self, value))

    def compute_value(self) -> Color:
        return Color(self.red, self.green, self.blue).clamped

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


class ColorPicker(Widget):
    DEFAULT_CSS = """
    ColorPicker > #color-preview {
        height: 10;
        width: 20;
    }
    """

    value = var(Color(r=0, g=0, b=0))

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

    def compose(self) -> ComposeResult:
        yield RgbTuner()
        yield Static(id="color-preview")

    def watch_value(self, value: Color) -> None:
        self.query_one("#color-preview").styles.background = value

    @on(RgbTuner.Changed)
    def on_rgb_tuner_changed(self, event: RgbTuner.Changed) -> None:
        self.value = event.value
