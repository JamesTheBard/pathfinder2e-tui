import webbrowser
from pathlib import Path

from textual import on
from textual.events import Event
from textual.widget import Widget
from textual.widgets import MarkdownViewer, Markdown, TextArea


class FeatsEditorWidget(TextArea):

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

    def on_text_area_changed(self, event: TextArea.Changed):
        markdown: MarkdownViewer = self.app.query_exactly_one("#featsdisplay")
        m = markdown.query_exactly_one(Markdown)
        m.update(self.text)

    def action_save_content(self):
        self.save_to_file(self.savefile)
        self.notify("Feats and spells saved.")
        markdown: MarkdownViewer = self.app.query_exactly_one("#featsdisplay")
        m = markdown.query_exactly_one(Markdown)
        m.update(self.text)


class FeatsMarkdown(MarkdownViewer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @on(Markdown.LinkClicked)
    def open_link(self, event: Markdown.LinkClicked):
        event.prevent_default()
        webbrowser.open(event.href, autoraise=False)
