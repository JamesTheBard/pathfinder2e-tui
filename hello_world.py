from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from widgets.data import cs
from widgets.stats_page import SavesWidget, SkillsWidget, StatsWidget


class CombatScreen(Screen):

    SUB_TITLE = "Combat"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("This is a test.")
        yield Footer()


class StatsScreen(Screen):

    SUB_TITLE = "Statistics"

    test = "Name: Kurosuke Ayame\nClass: Cleric 4"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(self.test, id="character-info")
        yield Static("HP stuff goes here", id="hp-stuff")
        yield StatsWidget(id="stats")
        yield SkillsWidget(id="skills")
        yield SavesWidget(id="saves")
        yield Footer()


class FeatsScreen(Screen):

    SUB_TITLE = "Feats"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("This is a test.")
        yield Footer()


class PF2eCharacterSheet(App):

    CSS_PATH = "styling/hello_world.tcss"

    BINDINGS = [
        ("f1", "switch_mode('stats_screen')", "Statistics"),
        ("f2", "switch_mode('combat_screen')", "Combat"),
        ("f3", "switch_mode('feats_screen')", "Feats"),
        ("ctrl+r", "refresh", "Refresh"),
        ("ctrl+q", "quit", "Quit"),
    ]
    MODES = {
        "stats_screen": StatsScreen,
        "combat_screen": CombatScreen,
        "feats_screen": FeatsScreen
    }

    TITLE = "PF2E Character Sheet"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def on_mount(self) -> None:
        self.switch_mode("stats_screen")

    def action_refresh(self) -> None:
        cs.refresh()


if __name__ == "__main__":
    app = PF2eCharacterSheet()
    app.run()
