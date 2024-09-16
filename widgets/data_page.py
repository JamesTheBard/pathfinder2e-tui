from pathlib import Path

import jsonschema
import jsonschema.exceptions
import yaml
from textual.widgets import TextArea
from rich.text import Text

from rules.helpers import Validator


class DataEditorWidget(TextArea):

    BINDINGS = [
        ("ctrl+s", "save_content", "Save"),
    ]

    def __init__(self, savefile, **kwargs):
        super().__init__(**kwargs)
        self.savefile = savefile
        self.load_from_file(self.savefile)
        self.language = "yaml"
        self.show_line_numbers = True
        self.tab_behavior = "indent"
        self.indent_width = 2

    def load_from_file(self, filename: str | Path):
        filename = Path(filename)
        try:
            self.text = filename.read_text()
        except FileNotFoundError:
            filename.touch()
            self.text = "Notes go here!"

    def save_to_file(self, filename: str | Path):
        try:
            content = yaml.safe_load(self.text)
            self.validate(content)
        except jsonschema.exceptions.ValidationError as e:
            message = f"[b]Validationo Error at '/{'/'.join(e.path)}'[/b]: {e.message}"
            self.notify(message, severity="error")
            return

        filename = Path(filename)
        filename.write_text(self.text)
        self.notify("Character sheet saved!")

    def action_save_content(self):
        self.save_to_file(self.savefile)

    def validate(self, content):
        v = Validator()
        v.validate(content)
