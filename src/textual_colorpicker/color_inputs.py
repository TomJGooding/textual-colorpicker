from textual.app import ComposeResult
from textual.color import HSV, Color
from textual.containers import Container, HorizontalGroup
from textual.reactive import var
from textual.widget import Widget
from textual.widgets import Input, Label


class RGBInputs(Widget):
    DEFAULT_CSS = """
    RGBInputs {
        width: auto;
        height: auto;

        HorizontalGroup {
            width: auto;
        }

        Label {
            padding: 1 0;
        }

        Input {
            width: 10;
        }
    }
    """

    color: var[Color] = var(Color(255, 0, 0), init=False)

    def compose(self) -> ComposeResult:
        r, g, b = self.color.rgb
        with HorizontalGroup():
            yield Label("R:")
            yield Input(str(r), id="--red-input")
        with HorizontalGroup():
            yield Label("G:")
            yield Input(str(g), id="--green-input")
        with HorizontalGroup():
            yield Label("B:")
            yield Input(str(b), id="--blue-input")

    def _watch_color(self) -> None:
        r, g, b = self.color.rgb
        self.query_one("#--red-input", Input).value = str(r)
        self.query_one("#--green-input", Input).value = str(g)
        self.query_one("#--blue-input", Input).value = str(b)


class HSVInputs(Widget):
    DEFAULT_CSS = """
    HSVInputs {
        width: auto;
        height: auto;

        HorizontalGroup {
            width: auto;
        }

        Label {
            padding: 1 0;
        }

        Input {
            width: 10;
        }
    }
    """

    hsv: var[HSV] = var(HSV(0.0, 1.0, 1.0), init=False)

    def compose(self) -> ComposeResult:
        h, s, v = self.hsv_values
        with HorizontalGroup():
            yield Label("H:")
            yield Input(str(h), id="--hue-input")
        with HorizontalGroup():
            yield Label("S:")
            yield Input(str(s), id="--saturation-input")
        with HorizontalGroup():
            yield Label("V:")
            yield Input(str(v), id="--value-input")

    def _watch_hsv(self) -> None:
        h, s, v = self.hsv_values
        self.query_one("#--hue-input", Input).value = str(h)
        self.query_one("#--saturation-input", Input).value = str(s)
        self.query_one("#--value-input", Input).value = str(v)

    @property
    def hsv_values(self) -> tuple[int, int, int]:
        h = int(self.hsv.h * 360 + 0.5)
        s = int(self.hsv.s * 100 + 0.5)
        v = int(self.hsv.v * 100 + 0.5)
        return (h, s, v)


class HexInput(Widget):
    DEFAULT_CSS = """
    HexInput {
        width: auto;
        height: auto;

        HorizontalGroup {
            width: auto;
        }

        Label {
            padding: 1 0;
        }

        Input {
            width: 13;
        }
    }
    """

    value: var[str] = var("ff0000", init=False)

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label("#")
            yield Input(self.value)

    def _watch_value(self, value: str) -> None:
        self.query_one(Input).value = value


class ColorInputs(Container):
    DEFAULT_CSS = """
    ColorInputs {
        width: auto;
        height: auto;

        HorizontalGroup {
            width: auto;
        }

        HexInput {
            margin-top: 1;
            margin-left: 1;
        }
    }
    """

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield RGBInputs()
            yield HSVInputs()
        yield HexInput()


if __name__ == "__main__":
    from textual.app import App

    class ColorInputsApp(App):
        CSS = """
        Screen {
            align: center middle;
        }
        """

        def compose(self) -> ComposeResult:
            yield ColorInputs()

    app = ColorInputsApp()
    app.run()
