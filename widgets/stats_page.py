from rich.text import Text
from textual.containers import Container, VerticalScroll
from textual.widget import Widget
from textual.widgets import Input, Label, Static

from rules.skills import Skill
from rules.stats import Save
from widgets.data import cs
from widgets.shared import TableWidget, fix_number, prof_map, stats_shorthand


class StatsWidget(TableWidget):

    def __init__(self, **kwargs) -> None:
        headers = ("", "Value", "Mod")
        content = self.format_data()
        border_title = "Statistics"
        super().__init__(headers, content, border_title, **kwargs)

    def format_data(self):
        for stat in stats_shorthand.keys():
            i = getattr(cs.stats, stat)
            yield (
                Text(stat.title()),
                Text(str(i), style="bold on grey19", justify="right"),
                Text(fix_number(cs.stats.get_modifier(stat)), justify="right"),
            )


class SkillsWidget(TableWidget):

    def __init__(self, **kwargs) -> None:
        headers = ("", "Total", "Stat", "Mod", "P", "Mod", "Misc", "Penalty")
        content = self.format_data()
        border_title = "Skills"
        super().__init__(headers, content, border_title, **kwargs)

    def format_data(self):
        i: Skill
        for i in cs.skills:
            yield [
                i.name,
                Text(fix_number(i.total), style="bold on grey19", justify="right"),
                Text(stats_shorthand[i.stat], justify="right"),
                Text(fix_number(i.modifier), justify="right"),
                Text(prof_map[i.proficiency], justify="right"),
                Text(fix_number(i.proficiency_bonus), justify="right"),
                Text(fix_number(i.bonus), justify="right"),
                Text(fix_number(i.check_penalty), justify="right"),
            ]


class SavesWidget(TableWidget):

    def __init__(self, **kwargs) -> None:
        headers = ("", "Total", "Stat", "Mod", "P", "Mod", "Item", "Misc")
        content = self.format_data()
        border_title = "Saves"
        super().__init__(headers, content, border_title, **kwargs)

    def format_data(self):
        i: Save
        for i in cs.saves:
            yield (
                i.name.title(),
                Text(fix_number(i.total), justify="right", style="bold on grey19"),
                Text(stats_shorthand[i.stat], justify="right"),
                Text(fix_number(i.modifier), justify="right"),
                Text(prof_map[i.proficiency], justify="right"),
                Text(fix_number(i.proficiency_bonus), justify="right"),
                Text(fix_number(i.item_bonus), justify="right"),
                Text(fix_number(i.bonus), justify="right"),
            )


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
            Text("  Class: ", style="bold"),
            Text(f" {cs.character.classes.title()} ", style="on #303030"),
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
        speed = cs.character.speed + cs.character.speed_bonus
        text = [
            Text(" Languages: ", style="bold"),
            Text(f" {', '.join(languages)} ", style="on #303030"),
            Text("  Speed: ", style="bold"),
            Text(f" {speed}' ", style="on #303030")
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
