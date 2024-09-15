from rich.text import Text
from textual.containers import Container, VerticalScroll
from textual.widget import Widget
from textual.widgets import Static, TabbedContent, TabPane, TextArea, Rule, Markdown

from widgets.data import cs
from widgets.shared import TableWidget, fix_number, prof_map, attack_map
from rules.helpers import format_keywords
from rules.weapons import Weapon

from typing import Iterable

class ArmorDataWidget(TableWidget):

    def __init__(self, **kwargs) -> None:
        headers = ("", "Mod")
        content = self.format_data()
        super().__init__(headers, content, None, **kwargs)

    def format_data(self):
        armor_map = {
            "ac_bonus": "AC Bonus",
            "proficiency_bonus": "Prof",
            "potency": "Potency",
            "dexterity": "Dex Bonus",
            "bonus": "Misc",
        }

        if cs.armor.dex_cap is not None:
            armor_map["dex_cap"] = "DEX Cap"

        if cs.armor.strength is not None:
            armor_map["strength"] = "Required STR"

        if cs.armor.check_penalty is not None:
            armor_map["check_penalty"] = "Check Penalty"

        for k, v in armor_map.items():
            if k in ["potency"]:
                yield (armor_map[k], Text(str(getattr(cs.armor, k)), justify="right"))
            else:
                yield (armor_map[k], Text(fix_number(getattr(cs.armor, k)), justify="right"))


class ShieldDataWidget(TableWidget):

    def __init__(self, **kwargs):
        headers = ("", "Value")
        content = self.format_data()
        super().__init__(headers, content, None, **kwargs)

    def format_data(self):
        yield ("Hardness", Text(str(cs.shield.hardness), justify="right"))
        yield ("Total HP", Text(str(cs.shield.total_hp), justify="right"))
        yield ("Broken HP", Text(str(cs.shield.total_hp // 2), justify="right"))


class ShieldWidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.border_title = "Shield"

    def compose(self):
        if cs.shield.name == "No Shield":
            yield Static(Text("No shield equipped."))

        yield Container(
            Static(Text(f"{cs.shield.name}: {fix_number(cs.shield.bonus)} AC\n", style="bold")),
            VerticalScroll(ShieldDataWidget(id="shielddata")),
        )


class ArmorWidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.border_title = "Armor"

    def compose(self):
        yield Container(
            Static(Text(f"{prof_map[cs.armor.proficiency]} {cs.armor.name}: {cs.armor.total} AC\n", "bold")),
            VerticalScroll(ArmorDataWidget(id="armordata"))
        )


class NotesWidget(TextArea):

    def __init__(self, **kwargs):
        self.content = ""
        super().__init__(self.content, **kwargs)
        self.border_title = "Notes"


class WeaponsWidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.border_title = "Weapons and Attacks"

    def compose(self):
        with TabbedContent():
            for w in cs.weapons:
                with TabPane(w.name):
                    yield VerticalScroll(
                        Static(self.build_attacks(weapon=w)),
                        Static(self.build_keywords(weapon=w)),
                        Static(self.build_source(weapon=w)),
                        Rule(),
                        Markdown("**Notes**: " + w.notes.replace("\n", "\n\n")),
                    )

    def build_attacks(self, weapon: Weapon):
        text = [
            Text(f"{prof_map[weapon.proficiency]} Attacks: ", style="bold"),
            Text(' ' + ', '.join(self.label_attacks(weapon.get_attacks)) + ' ', style="on #303030"),
            Text("  "),
            Text("Damage: ", style="bold "),
            Text(f" {weapon.get_damage} ", style="on #303030"),
            Text("  "),
            Text(f"Type: ", style="bold"),
            Text(f" {weapon.weapon_type.title()} \n", style="on #303030"),
            Text('  Damage Type: ', style="bold"),
            Text(f" {weapon.damage_type} ", style="on #303030"),
        ]

        if weapon.weapon_type.casefold() in ["melee", "ranged"]:
            text.extend([
                Text('  Potency: ', style="bold"),
                Text(f" {weapon.potency} ", style="on #303030"),
                Text('  Striking: ', style="bold"),
                Text(f" {weapon.striking} ", style="on #303030"),
            ])

        return Text().join(text)
    
    def build_keywords(self, weapon: Weapon):
        label = Text('  Keywords: ', style="bold")
        keywords = Text(', '.join(format_keywords(weapon.keywords)))
        return Text().join((label, keywords))
    
    def build_source(self, weapon: Weapon):
        text = [
            
            Text('  Source: ', style="bold"),
            Text(weapon.source),
        ]
        return Text().join(text)
    
    def label_attacks(self, attacks: Iterable[str]) -> Iterable[str]:
        return [f"{attack_map[i]} {v}" for i, v in enumerate(attacks)]
            