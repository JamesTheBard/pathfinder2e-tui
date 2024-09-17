from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable
from rules.helpers import fix_number


prof_map = {
    "untrained": "🅄",
    "trained": "🆃",
    "expert": "🅴",
    "master": "🅼",
    "legendary": "🅻",
}


action_map = {
    "reaction": "🅁",
    "free": "🄵",
    "1": "➊",
    "2": "➋",
    "3": "➌",
}

attack_map = ["➀", "➁", "➂"]

stats_shorthand = {
    "strength": "STR",
    "dexterity": "DEX",
    "constitution": "CON",
    "intelligence": "INT",
    "wisdom": "WIS",
    "charisma": "CHA",
}

class TableWidget(Widget):

    def __init__(self, header, content, title, **kwargs) -> None:
        super().__init__(**kwargs)
        self.header = header
        self.content = content
        self.border_title = title

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self, clear: bool = False):
        table = self.query_one(DataTable)
        if clear:
            table.clear(True)
        table.add_columns(*self.header)
        table.show_header = True
        table.add_rows(self.content)
        table.zebra_stripes = True
        table.cursor_type = "row"
        table.show_cursor = False

    def action_refresh(self):
        self.content = self.format_data()
        self.on_mount(clear=True)
