from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Static, TabbedContent, TabPane, Markdown, TextArea
from textual.containers import VerticalScroll

from widgets.data import cs
from widgets.stats_page import SavesWidget, SkillsWidget, StatsWidget
from widgets.weapons_page import ArmorWidget, ShieldWidget, NotesWidget, WeaponsWidget
from widgets.notes_page import NoteEditorWidget

from widgets.data import cs


class CombatScreen(Screen):

    SUB_TITLE = "Combat"

    def compose(self) -> ComposeResult:
        yield Header()
        yield ArmorWidget(id="armor")
        # yield Placeholder("Weapons go here", id="weapon")
        yield WeaponsWidget(id="weapon")
        yield ShieldWidget(id="shield")
        yield NotesWidget(id="notes")
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


class NotesScreen(Screen):

    SUB_TITLE = "Notes"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with TabbedContent():
            with TabPane("Notes"):
                yield VerticalScroll(
                    Markdown("# This is a test.", id="testid")
                )
            with TabPane("Editor"):
                yield VerticalScroll(
                    NoteEditorWidget()
                )


class PF2eCharacterSheet(App):

    CSS_PATH = "styling/hello_world.tcss"

    BINDINGS = [
        ("f1", "switch_mode('stats_screen')", "Statistics"),
        ("f2", "switch_mode('combat_screen')", "Combat"),
        ("f3", "switch_mode('feats_screen')", "Feats"),
        ("f4", "switch_mode('notes_screen')", "Notes"),
        ("ctrl+r", "refresh", "Refresh"),
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


if __name__ == "__main__":
    cs.load_character_sheet('characters/info.yaml')
    cs.load_file_as_text('characters/feats.md', "feats")
    cs.load_file_as_text('characters/notes.txt', "notes")
    app = PF2eCharacterSheet()
    app.run()
