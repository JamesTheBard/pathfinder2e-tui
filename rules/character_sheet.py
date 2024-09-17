from pathlib import Path
from typing import Iterable, Generator

import yaml
from box import Box

from rules.armor import Armor, ArmorMixin, Shield
from rules.skills import Skill, SkillsMixin
from rules.stats import (HitPoints, HitPointsMixin, Names, NamesMixin, Save,
                         SavesMixin, Stats, StatsMixin)
from rules.weapons import Weapon, WeaponsMixin


class CharacterSheet(HitPointsMixin, NamesMixin, SkillsMixin, StatsMixin, SavesMixin, ArmorMixin, WeaponsMixin):
    """The PF2E Character sheet class.  Responsible for calculating all of the
    character information and processing all of the entries in the character
    data file.

    Attributes:
        armor (Armor): The armor the character currently has equipped
        character_class (int): The class of the character
        character_level (int): The level of the character
        character (Names): The misc information about the character (e.g. name, player, ...)
        current_hp (int): The current HP total of the character
        data (Box): The raw, unprocessed data from the character info file
        hp (HitPoints): The HP information of the character
        saves (Generator[Save, None, None]): Save and Perception information
        shield (Shield): Shield information of the character
        skills (Generator[Skill, None, None]): Skill information of the character
        stats (Stats): The statistics (e.g. "strength") of the character
        weapons (Generator[Weapon, None, None]): Weapon/attack information
        yaml_file (Path): The character information file location
    """

    armor: Armor
    character: Names
    current_hp: int
    data: Box
    hp: HitPoints
    saves: Generator[Save, None, None]
    shield: Shield
    skills: Generator[Skill, None, None]
    stats: Stats
    weapons: Generator[Weapon, None, None]
    yaml_file: Path

    def __init__(self) -> None:
        super().__init__()

    def load_character_sheet(self, yaml_file: Path | str) -> None:
        """Load the character information from a YAML file.

        Args:
            yaml_file (Path | str): The YAML file to load
        """
        self.yaml_file = Path(yaml_file)
        with self.yaml_file.open('r') as f:
            self.data = Box(yaml.safe_load(f))
        self.character = self.process_names()
        self.stats = self.process_stats()
        self.hp = self.process_hit_points()
        self.armor = self.get_armor()
        self.shield = self.get_shield()
        self.skills = self.process_skills()
        self.saves = self.process_saves()
        self.weapons = self.process_weapons()
        self.current_hp = self.hp.total

    def load_file_as_text(self, filename: Path | str, attrib: str) -> None:
        """Load the contents of a text file into an attribute 'attrib'

        Args:
            filename (Path | str): The file to load
            attrib (str): The attribute to store the data in
        """
        try:
            setattr(self, attrib, Path(filename).read_text())
        except FileNotFoundError:
            Path(filename).touch()
            setattr(self, attrib, "")

    def refresh(self) -> None:
        """Recalculate all data in the character sheet
        """
        current_hp = self.current_hp
        self.load_character_sheet(self.yaml_file)
        self.current_hp = current_hp

    def get_proficiency(self, proficiency: str = "untrained") -> int:
        """Calculate the proficiency modifier given a proficiency level (e.g. "trained")

        Args:
            proficiency (str): The proficiency level. Defaults to "untrained".

        Returns:
            int: The modifier of the proficiency level
        """

        bonus_map = {
            "untrained": 0,
            "trained": 2,
            "expert": 4,
            "master": 6,
            "legendary": 8,
        }

        try:
            bonus = bonus_map[proficiency]
        except:
            return 0

        if proficiency not in bonus_map.keys() or proficiency == "untrained":
            return bonus_map[proficiency]
        return bonus_map[proficiency] + self.character.character_level

    def process_keywords(self, keywords: str | Iterable[str]) -> tuple[str]:
        """Process the keywords entry and convert it to a default format (tuple)

        Args:
            keywords (str | Iterable[str]): The keywords to process

        Returns:
            tuple[str]: A tuple of keywords
        """
        if isinstance(keywords, str):
            keywords = [i.strip() for i in keywords.split(',')]
        return [i.casefold() for i in keywords]
