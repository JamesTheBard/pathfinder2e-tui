from dataclasses import dataclass
from typing import Optional
import re
import sys
import logging


@dataclass
class Armor:
    name: str
    keywords: list[str]
    ac_bonus: int = 0
    check_penalty: int = 0
    dex_cap: Optional[int] = None
    strength: Optional[int] = None
    equipped: bool = True
    potency: int = 0
    bonus: int = 0
    proficiency: str = "untrained"
    proficiency_bonus: int = 0
    dexterity: int = 0

    @property
    def total(self):
        return 10 + self.ac_bonus + self.potency + self.bonus + self.dexterity + self.proficiency_bonus


@dataclass
class Shield:
    name: str
    bonus: int = 0
    hardness: int = 0
    total_hp: int = 0


class ArmorMixin:

    def get_armor(self):
        regex = re.compile(r'armou{0,1}r$')
        armor_string = next((i for i in self.data.keys() if regex.match(i)), None)
        if not armor_string:
            logging.fatal("Character sheet must have an armor/armour section!")
            sys.exit(2)
        data = self.data.get(armor_string)

        dexterity = self.stats.get_modifier("dexterity")
        if (cap := data.get("dex_cap", None)) != None:
            dexterity = min(dexterity, cap)

        if (keywords := data.get("keywords", list())) == None:
            keywords = list()

        keywords = self.process_keywords(keywords)

        return Armor(
            name=data.get("name"),
            proficiency=data.get("proficiency", "untrained"),
            proficiency_bonus=self.get_proficiency(data.get("proficiency", "untrained")),
            keywords=list(keywords),
            ac_bonus=data.get("ac_bonus", 0),
            dex_cap=data.get("dex_cap", None),
            strength=data.get("strength", None),
            check_penalty=data.get("check_penalty", 0),
            equipped=data.get("equipped", True),
            potency=data.get("potency", 0),
            bonus=data.get("bonus", 0),
            dexterity=dexterity,
        )

    def get_shield(self):
        try:
            data = self.data.get("shield", dict())
        except AttributeError:
            data = dict()

        if not data:
            return Shield(name="No Shield")

        return Shield(
            name=data.get("name"),
            bonus=data.get("bonus", 0),
            hardness=data.get("hardness", 0),
            total_hp=data.get("total_hp", 0),
        )
