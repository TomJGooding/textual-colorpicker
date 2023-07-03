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
from textual_slider import Slider


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
        text-style: bold;
    }

    RgbTuner #red-slider .slider--slider {
        color: red;
    }

    RgbTuner #green-slider .slider--slider {
        color: green;
    }

    RgbTuner #blue-slider .slider--slider {
        color: blue;
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
            yield Slider(min=0, max=255, id="red-slider")
            yield RgbInput(str(0), id="red-input", classes="input")
        with Horizontal():
            yield Label("G")
            yield Slider(min=0, max=255, id="green-slider")
            yield RgbInput(str(0), id="green-input", classes="input")
        with Horizontal():
            yield Label("B")
            yield Slider(min=0, max=255, id="blue-slider")
            yield RgbInput(str(0), id="blue-input", classes="input")

    @on(RgbInput.Changed)
    def on_rgb_input_changed(self, event: RgbInput.Changed) -> None:
        assert event.validation_result is not None
        if not event.validation_result.is_valid:
            return
        new_value: int = int(event.value)
        if event.input.id == "red-input":
            self.red = new_value
            red_slider = self.query_one("#red-slider", Slider)
            with red_slider.prevent(Slider.Changed):
                red_slider.value = new_value
        elif event.input.id == "green-input":
            self.green = new_value
            green_slider = self.query_one("#green-slider", Slider)
            with green_slider.prevent(Slider.Changed):
                green_slider.value = new_value
        elif event.input.id == "blue-input":
            self.blue = new_value
            blue_slider = self.query_one("#blue-slider", Slider)
            with blue_slider.prevent(Slider.Changed):
                blue_slider.value = new_value

    @on(Slider.Changed)
    def on_rgb_slider_changed(self, event: Slider.Changed) -> None:
        new_value: int = event.value
        if event.slider.id == "red-slider":
            self.red = new_value
            red_input = self.query_one("#red-input", RgbInput)
            with red_input.prevent(Input.Changed):
                red_input.value = str(new_value)
        elif event.slider.id == "green-slider":
            self.green = new_value
            green_input = self.query_one("#green-input", RgbInput)
            with green_input.prevent(Input.Changed):
                green_input.value = str(new_value)
        elif event.slider.id == "blue-slider":
            self.blue = new_value
            blue_input = self.query_one("#blue-input", RgbInput)
            with blue_input.prevent(Input.Changed):
                blue_input.value = str(new_value)


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
