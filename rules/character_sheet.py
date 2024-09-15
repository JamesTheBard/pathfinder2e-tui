from pathlib import Path
from typing import Optional

import yaml
from box import Box

from rules.armor import ArmorMixin
from rules.skills import SkillsMixin
from rules.stats import HitPointsMixin, NamesMixin, SavesMixin, StatsMixin
from rules.weapons import WeaponsMixin


class CharacterSheet(HitPointsMixin, NamesMixin, SkillsMixin, StatsMixin, SavesMixin, ArmorMixin, WeaponsMixin):

    def __init__(self) -> None:
        super().__init__()

    def load_character_sheet(self, yaml_file: Path | str):
        self.yaml_file = Path(yaml_file)
        with self.yaml_file.open('r') as f:
            self.data = Box(yaml.safe_load(f))
        self.level = sum(int(i.split(' ')[-1])
                         for i in self.data.character.classes)
        self.stats = self.process_stats()
        self.hp = self.process_hit_points()
        self.armor = self.get_armor()
        self.shield = self.get_shield()
        self.skills = self.process_skills()
        self.saves = self.process_saves()
        self.weapons = self.process_weapons()
        self.character = self.process_names()
        self.current_hp = self.hp.total

    def load_file_as_text(self, filename: Path | str, attrib: str):
        try:
            setattr(self, attrib, Path(filename).read_text())
        except FileNotFoundError:
            Path(filename).touch()
            setattr(self, attrib, "")

    def refresh(self):
        current_hp = self.current_hp
        self.load_character_sheet(self.yaml_file)
        self.current_hp = current_hp

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
