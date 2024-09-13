from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable


def fix_number(number: int, ignore_zero=False) -> str:
    if number == 0 and not ignore_zero:
        return '0'
    return str(number) if number < 0 else f'+{number}'


prof_map = {
    "untrained": "🅄",
    "trained": "🆃",
    "expert": "🅴",
    "master": "🅼",
    "legendary": "🅻",
}


class TableWidget(Widget):

    def __init__(self, header, content, title, **kwargs) -> None:
        super().__init__(**kwargs)
        self.header = header
        self.content = content
        self.border_title = title

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self):
        table = self.query_one(DataTable)
        table.add_columns(*self.header)
        table.show_header = True
        table.add_rows(self.content)
        table.zebra_stripes = True
