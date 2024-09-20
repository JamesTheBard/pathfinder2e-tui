import webbrowser
from pathlib import Path

from textual import on
from textual.events import Event
from textual.widget import Widget
from textual.widgets import MarkdownViewer, Markdown, TextArea


class SpellsEditorWidget(TextArea):

    BINDINGS = [
        ("ctrl+s", "save_content", "Save"),
    ]

    def __init__(self, savefile, **kwargs):
        super().__init__(**kwargs)
        self.savefile = savefile
        self.load_from_file(self.savefile)
        self.language = "markdown"
        self.show_line_numbers = True
        self.tab_behavior = "indent"
        self.indent_width = 4

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
        mv: MarkdownViewer = self.app.query_exactly_one("#spellsdisplay")
        v: Markdown = mv.query_exactly_one(Markdown)
        v.update(content)

    def action_save_content(self):
        self.save_to_file(self.savefile)
        self.notify("Spells saved.")
        self.update_markdown(self.text)


class SpellsMarkdown(MarkdownViewer):

    def __init__(self, savefile, **kwargs):
        super().__init__(Path(savefile).read_text(), **kwargs)

    @on(Markdown.LinkClicked)
    def open_link(self, event: Markdown.LinkClicked):
        event.prevent_default()
        webbrowser.open(event.href, autoraise=False)
