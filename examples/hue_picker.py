from textual.app import App, ComposeResult

from textual_colorpicker.hue_picker import HuePicker


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


if __name__ == "__main__":
    app = HuePickerApp()
    app.run()
