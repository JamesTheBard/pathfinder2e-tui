from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable


prof_map_linux = {
    "untrained": "🅄",
    "trained": "🆃",
    "expert": "🅴",
    "master": "🅼",
    "legendary": "🅻",
}

prof_map_windows = [i[0].upper() for i in prof_map_linux]

action_map_linux = {
    "reaction": "🅁",
    "free": "🄵",
    "1": "➊",
    "2": "➋",
    "3": "➌",
}

action_map_windows = {
    "reaction": "R",
    "free": "F",
    "1": "1",
    "2": "2",
    "3": "3",
}

attack_map_linux = ["➀", "➁", "➂"]
attack_map_windows = ["1", "2", "3"]

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
