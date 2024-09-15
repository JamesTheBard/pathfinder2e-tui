import webbrowser
from pathlib import Path

from textual import on
from textual.events import Event
from textual.widget import Widget
from textual.widgets import Markdown, TextArea


class NoteEditorWidget(TextArea):

    BINDINGS = [
        ("ctrl+s", "save_content", "Save"),
    ]

    def __init__(self, savefile, **kwargs):
        super().__init__(**kwargs)
        self.savefile = savefile
        self.load_from_file(self.savefile)

    def load_from_file(self, filename: str | Path):
        filename = Path(filename)
        try:
            self.text = filename.read_text()
        except FileNotFoundError:
            filename.touch()
            self.text = "Notes go here!"

    def save_to_file(self, filename: str | Path):
        filename = Path(filename)
        filename.write_text(self.text)

    def on_text_area_changed(self, event: TextArea.Changed):
        markdown = self.app.query_exactly_one("#notesdisplay")
        markdown.update(self.text)

    def action_save_content(self):
        self.save_to_file(self.savefile)
        self.notify("Notes saved.")


class NotesMarkdown(Markdown):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @on(Markdown.LinkClicked)
    def open_link(self, event: Markdown.LinkClicked):
        webbrowser.open(event.href, autoraise=False)
