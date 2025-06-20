# textual-colorpicker

A color picker widget for [Textual](https://github.com/Textualize/textual).

![screenshot](https://raw.githubusercontent.com/TomJGooding/textual-colorpicker/main/assets/screenshot.png)

## Installation

Install textual-colorpicker using pip:

```
pip install textual-colorpicker
```

## Usage

textual-colorpicker provides a `ColorPicker` widget for use in Textual.

```python
from textual.app import App, ComposeResult

from textual_colorpicker import ColorPicker


class ColorPickerApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield ColorPicker()


if __name__ == "__main__":
    app = ColorPickerApp()
    app.run()
```

## Limitations

Textual apps run in the terminal, which work in terms of character cells rather
than pixels. This means you obviously can't have the same fine-grained control
with the mouse for this color picker as usual.

## Contributing

I created this color picker widget as a learning exercise to better understand
Textual and it is still a work in progress.

I'd really appreciate any feedback or suggestions, but I'm afraid I probably
won't be accepting any PRs at the moment.

## License

Licensed under the [GNU General Public License v3.0](LICENSE).
