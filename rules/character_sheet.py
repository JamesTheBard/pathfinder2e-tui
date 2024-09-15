import math
import yaml
from rules.skills import SkillsMixin
from rules.stats import StatsMixin, SavesMixin
from rules.armor import ArmorMixin
from rules.weapons import WeaponsMixin
from pathlib import Path
from typing import Optional

from box import Box


class CharacterSheet(SkillsMixin, StatsMixin, SavesMixin, ArmorMixin, WeaponsMixin):

    def __init__(self) -> None:
        super().__init__()

    def load_character_sheet(self, yaml_file: Path | str):
        self.yaml_file = Path(yaml_file)
        with self.yaml_file.open('r') as f:
            self.data = Box(yaml.safe_load(f))
        self.level = sum(int(i.split(' ')[-1])
                         for i in self.data.character.classes)
        self.stats = self.process_stats()
        self.armor = self.get_armor()
        self.shield = self.get_shield()
        self.skills = self.process_skills()
        self.saves = self.process_saves()
        self.weapons = self.process_weapons()

    def load_file_as_text(self, filename: Path | str, attrib: str):
        try:
            setattr(self, attrib, Path(filename).read_text())
        except FileNotFoundError:
            Path(filename).touch()
            setattr(self, attrib, "")

    def refresh(self):
        self.load_character_sheet(self.yaml_file)

    def get_proficiency(self, prof_level: Optional[str] = "untrained"):
        bonus_map = {
            "untrained": 0,
            "trained": 2,
            "expert": 4,
            "master": 6,
            "legendary": 8,
        }

        try:
            bonus = bonus_map[prof_level]
        except:
            return 0

        if prof_level not in bonus_map.keys() or prof_level == "untrained":
            return bonus_map[prof_level]
        return bonus_map[prof_level] + self.level
    
    def process_keywords(self, keywords: str | list | tuple) -> list:
        if isinstance(keywords, str):
            keywords = [i.strip() for i in keywords.split(',')]
        return [i.casefold() for i in keywords]
