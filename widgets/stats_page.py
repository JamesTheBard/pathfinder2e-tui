from rich.text import Text

from widgets.data import cs
from widgets.shared import TableWidget, fix_number, prof_map
from textual.widget import Widget
from textual.widgets import Static, Input, Label, Rule
from textual.containers import VerticalScroll, Container


class StatsWidget(TableWidget):

    def __init__(self, **kwargs) -> None:
        headers = ("", "Value", "Mod")
        content = self.format_data()
        border_title = "Statistics"
        super().__init__(headers, content, border_title, **kwargs)

    def format_data(self):
        for i in cs.stats.data:
            i = list(i)
            i[1] = Text(str(i[1]), style="bold on grey19", justify="right")
            i[2] = Text(fix_number(i[2]), justify="right")
            yield i


class SkillsWidget(TableWidget):

    def __init__(self, **kwargs) -> None:
        headers = ("", "Total", "Stat", "Mod", "P", "Mod", "Misc", "Penalty")
        content = self.format_data()
        border_title = "Skills"
        super().__init__(headers, content, border_title, **kwargs)

    def format_data(self):
        for i in cs.skills:
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
        content = self.format_data()
        border_title = "Saves"
        super().__init__(headers, content, border_title, **kwargs)

    def format_data(self):
        for i in cs.saves:
            i = list(i.data)
            i[1] = Text(fix_number(i[1]), justify="right", style="bold on grey19")
            i[2] = Text(i[2], justify="right")
            i[3] = Text(fix_number(i[3]), justify="right")
            i[4] = Text(prof_map[i[4]], justify="right")
            i[5] = Text(fix_number(i[5]), justify="right")
            i[6] = Text(fix_number(i[6]), justify="right")
            i[7] = Text(fix_number(i[7]), justify="right")
            yield i


class NameWidget(Widget):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.border_title = "Character"
        self.add_class("refreshable")

    def compose(self):
        yield VerticalScroll(
            Static(self.build_name_class()),
            Static(self.build_background()),
            Static(self.build_languages()),
        )

    def action_refresh(self):
        self.refresh(recompose=True)

    def build_name_class(self):
        text = [
            Text(" Name: ", style="bold"),
            Text(f" {cs.character.name} ", style="on #303030"),
            Text("  Classes: ", style="bold"),
            Text(f" {', '.join(cs.character.classes)} ", style="on #303030"),
        ]
        if cs.character.diety:
            text.extend([
                Text("  Diety: ", style="bold"),
                Text(f" {cs.character.diety.title()} ", style="on #303030")
            ])

        return Text().join(text)

    def build_background(self):
        text = [
            Text(" Ancestry: ", style="bold"),
            Text(f" {cs.character.ancestry.title()} ", style="on #303030"),
            Text("  Background: ", style="bold"),
            Text(f" {cs.character.background.title()} ", style="on #303030"),
            Text("  Heritage: ", style="bold"),
            Text(f" {cs.character.heritage.title()} ", style="on #303030"),
        ]
        return Text().join(text)

    def build_languages(self):
        languages = [i.title() for i in cs.character.languages]
        text = [
            Text(" Languages: ", style="bold"),
            Text(f" {', '.join(languages)} ", style="on #303030")
        ]
        return Text().join(text)


class CurrentHP(Input):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "integer"
        self.value = str(cs.current_hp)

    def action_submit(self):
        cs.current_hp = self.value


class HitPointWidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.border_title = "Vitals"
        self.add_class("refreshable")

    def action_refresh(self):
        self.refresh(recompose=True)

    def compose(self):
        yield Label(self.build_hp())
        yield Container(
            Label(Text(" Current HP: ", style="bold")),
            CurrentHP(id="testhp"),
            id="hitpoints"
        )
        yield Static(self.build_rest())

    def build_hp(self):
        text = [
            Text(" Total HP:   ", style="bold"),
            Text(f" {cs.hp.total:<4} ", style="on #303030"),
        ]
        return Text().join(text)

    def build_rest(self):
        text = [
            Text(" Rest: ", style="bold"),
            Text(f" {fix_number(cs.hp.rest)} HP ", style="on #303030"),
        ]
        return Text().join(text)
