from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Static, TabbedContent, TabPane

from widgets.data import cs
from widgets.notes_page import NoteEditorWidget, NotesMarkdown
from widgets.stats_page import (HitPointWidget, NameWidget, SavesWidget,
                                SkillsWidget, StatsWidget)
from widgets.weapons_page import (ArmorWidget, NotesWidget, ShieldWidget,
                                  WeaponsWidget)
from widgets.data_page import DataEditorWidget
from widgets.feats_page import FeatsEditorWidget, FeatsMarkdown


class CombatScreen(Screen):

    SUB_TITLE = "Combat"

    def compose(self) -> ComposeResult:
        yield Header()
        yield ArmorWidget(id="armor", classes="refreshable")
        yield WeaponsWidget(id="weapon", classes="refreshable")
        yield ShieldWidget(id="shield", classes="refreshable")
        yield NotesWidget(id="notes")
        yield Footer()


class StatsScreen(Screen):

    SUB_TITLE = "Statistics"

    def compose(self) -> ComposeResult:
        yield Header()
        yield NameWidget(id="character-info")
        yield HitPointWidget(id="hp-stuff")
        yield StatsWidget(id="stats", classes="refreshable")
        yield SkillsWidget(id="skills", classes="refreshable")
        yield SavesWidget(id="saves", classes="refreshable")
        yield Footer()


class NotesScreen(Screen):

    SUB_TITLE = "Notes"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with TabbedContent():
            with TabPane("Notes"):
                yield VerticalScroll(
                    NotesMarkdown(id="notesdisplay")
                )
            with TabPane("Editor"):
                yield VerticalScroll(
                    NoteEditorWidget(savefile="characters/notes.md")
                )


class FeatsScreen(Screen):

    SUB_TITLE = "Feats and Spells"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with TabbedContent():
            with TabPane("Feats"):
                yield VerticalScroll(
                    FeatsMarkdown(id="featsdisplay")
                )
            with TabPane("Editor"):
                yield VerticalScroll(
                    FeatsEditorWidget(savefile="characters/feats.md")
                )


class DataScreen(Screen):

    SUB_TITLE = "Character Data"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield DataEditorWidget(savefile="characters/info.yaml")
        

class PF2eCharacterSheet(App):

    CSS_PATH = "styling/hello_world.tcss"

    BINDINGS = [
        ("f1", "switch_mode('stats_screen')", "Statistics"),
        ("f2", "switch_mode('combat_screen')", "Combat"),
        ("f3", "switch_mode('notes_screen')", "Notes"),
        ("f4", "switch_mode('feats_screen')", "Feats/Spells"),
        ("f5", "switch_mode('data_screen')", "Data"),
        ("ctrl+r", "refresh", "Reload"),
        ("ctrl+q", "quit", "Quit"),
    ]
    MODES = {
        "stats_screen": StatsScreen,
        "combat_screen": CombatScreen,
        "notes_screen": NotesScreen,
        "feats_screen": FeatsScreen,
        "data_screen": DataScreen
    }

    TITLE = "PF2E Character Sheet"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def on_mount(self) -> None:
        self.switch_mode("stats_screen")

    def action_refresh(self) -> None:
        cs.refresh()
        widgets = self.query(".refreshable")
        for w in widgets:
            w.action_refresh()
        self.notify("Character sheet reloaded.")


if __name__ == "__main__":
    cs.load_character_sheet('characters/info.yaml')
    app = PF2eCharacterSheet()
    app.run()
