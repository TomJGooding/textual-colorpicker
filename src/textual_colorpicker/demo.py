from textual.app import App, ComposeResult

from textual_colorpicker.colorpicker import ColorPicker


class ColorPickerApp(App):
    CSS = """
        Screen {
            align: center middle;
        }
    """

    def compose(self) -> ComposeResult:
        yield ColorPicker()

    def on_mount(self) -> None:
        self.query_one(ColorPicker).focus()
