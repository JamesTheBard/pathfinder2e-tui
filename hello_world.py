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

    test = "Name: Kurosuke Ayame\nClass: Cleric 4"

    def compose(self) -> ComposeResult:
        yield Header()
        yield NameWidget(id="character-info")
        yield HitPointWidget(id="hp-stuff")
        yield StatsWidget(id="stats", classes="refreshable")
        yield SkillsWidget(id="skills", classes="refreshable")
        yield SavesWidget(id="saves", classes="refreshable")
        yield Footer()


class FeatsScreen(Screen):

    SUB_TITLE = "Feats"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("This is a test.")
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


class PF2eCharacterSheet(App):

    CSS_PATH = "styling/hello_world.tcss"

    BINDINGS = [
        ("f1", "switch_mode('stats_screen')", "Statistics"),
        ("f2", "switch_mode('combat_screen')", "Combat"),
        ("f3", "switch_mode('feats_screen')", "Feats"),
        ("f4", "switch_mode('notes_screen')", "Notes"),
        ("ctrl+r", "refresh", "Reload"),
        ("ctrl+q", "quit", "Quit"),
    ]
    MODES = {
        "stats_screen": StatsScreen,
        "combat_screen": CombatScreen,
        "feats_screen": FeatsScreen,
        "notes_screen": NotesScreen,
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


if __name__ == "__main__":
    cs.load_character_sheet('characters/info.yaml')
    cs.load_file_as_text('characters/feats.md', "feats")
    app = PF2eCharacterSheet()
    app.run()
