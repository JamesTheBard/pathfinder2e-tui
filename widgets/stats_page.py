from rich.text import Text

from widgets.data import cs
from widgets.shared import TableWidget, fix_number, prof_map


class StatsWidget(TableWidget):

    def __init__(self, **kwargs) -> None:
        headers = ("", "Value", "Mod")
        content = self.format_data(cs.stats.data)
        border_title = "Statistics"
        super().__init__(headers, content, border_title, **kwargs)

    def format_data(self, content):
        for i in content:
            i = list(i)
            i[1] = Text(str(i[1]), style="bold on grey19", justify="right")
            i[2] = Text(fix_number(i[2]), justify="right")
            yield i


class SkillsWidget(TableWidget):

    def __init__(self, **kwargs) -> None:
        headers = ("", "Total", "Stat", "Mod", "P", "Mod", "Misc", "Penalty")
        content = self.format_data(cs.skills)
        border_title = "Skills"
        super().__init__(headers, content, border_title, **kwargs)

    def format_data(self, content):
        for i in content:
            i = list(i.data)
            i[1] = Text(fix_number(i[1]), style="bold on grey19", justify="right")
            i[2] = Text(i[2], justify="right")
            i[3] = Text(fix_number(i[3]), justify="right")
            i[4] = Text(prof_map[i[4]], justify="right")
            i[5] = Text(fix_number(i[5]), justify="right")
            i[6] = Text(fix_number(i[6]), justify="right")
            i[7] = Text(fix_number(i[7]), justify="right")
            yield i


class SavesWidget(TableWidget):

    def __init__(self, **kwargs) -> None:
        headers = ("", "Total", "Stat", "Mod", "P", "Mod", "Item", "Misc")
        content = self.format_data(cs.saves)
        border_title = "Saves"
        super().__init__(headers, content, border_title, **kwargs)

    def format_data(self, content):
        for i in content:
            i = list(i.data)
            i[1] = Text(fix_number(i[1]), justify="right", style="bold on grey19")
            i[2] = Text(i[2], justify="right")
            i[3] = Text(fix_number(i[3]), justify="right")
            i[4] = Text(prof_map[i[4]], justify="right")
            i[5] = Text(fix_number(i[5]), justify="right")
            i[6] = Text(fix_number(i[6]), justify="right")
            i[7] = Text(fix_number(i[7]), justify="right")
            yield i
