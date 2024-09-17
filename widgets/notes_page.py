import webbrowser
from pathlib import Path

from textual import on
from textual.events import Event
from textual.widget import Widget
from textual.widgets import MarkdownViewer, Markdown, TextArea


class NoteEditorWidget(TextArea):

    BINDINGS = [
        ("ctrl+s", "save_content", "Save"),
    ]

    def __init__(self, savefile, **kwargs):
        super().__init__(**kwargs)
        self.savefile = savefile
        self.load_from_file(self.savefile)
        self.language = "markdown"
        self.show_line_numbers = True

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

    def update_markdown(self, content):
        mv: MarkdownViewer = self.app.query_exactly_one("#notesdisplay")
        v: Markdown = mv.query_exactly_one(Markdown)
        v.update(content)

    def action_save_content(self):
        self.save_to_file(self.savefile)
        self.notify("Notes saved.")
        self.update_markdown(self.text)


class NotesMarkdown(MarkdownViewer):

    def __init__(self, savefile, **kwargs):
        super().__init__(Path(savefile).read_text(), **kwargs)

    @on(Markdown.LinkClicked)
    def open_link(self, event: Markdown.LinkClicked):
        event.prevent_default()
        webbrowser.open(event.href, autoraise=False)
