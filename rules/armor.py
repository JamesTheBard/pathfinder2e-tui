from dataclasses import dataclass
from typing import Optional
import re
import sys
import logging


@dataclass
class Armor:
    """The armor data class that holds all armor information

    Attributes:
        name (str): The name of the armor
        keywords (list[str] | str): The keywords associated with the armor
        ac_bonus (int): The AC bonus provided by the armor. Defaults to 0.
        bonus (int): The misc bonus to ac. Defaults to 0.
        check_penalty (int): The check penalty of the armor. Defaults to 0.
        dex_cap (Optional[int]): The dexterity cap of the armor.
        dexterity (int): The dexterity bonus for the character. Defaults to 0.
        equipped (bool): Whether the armor is equipped. Defaults to True.
        potency (int): The potency bonus for any runes equipped. Defaults to 0.
        proficiency_bonus (int): The proficiency bonus for the armor. Defaults to 0.
        proficiency (str): The proficiency for the armor. Defaults to "untrained".
        strength (Optional[int]): The required strength to avoid the check penalty. Defaults to None.
    """
    name: str
    keywords: list[str] | str
    ac_bonus: int = 0
    bonus: int = 0
    check_penalty: int = 0
    dex_cap: Optional[int] = None
    dexterity: int = 0
    equipped: bool = True
    potency: int = 0
    proficiency_bonus: int = 0
    proficiency: str = "untrained"
    strength: Optional[int] = None

    @property
    def total(self) -> int:
        """Return the current total AC with the equipped armor.

        Returns:
            int: The total AC
        """
        return 10 + self.ac_bonus + self.potency + self.bonus + self.dexterity + self.proficiency_bonus


@dataclass
class Shield:
    """The shield dataclass with all shield information

    Attributes:
        name (str): The name of the shield.
        bonus (int): The AC bonus of the shield when raised. Defaults to 0.
        hardness (int): The hardness of the shield. Defaults to 0.
        total_hp (int): The total amount of HP the shield has. Defaults to 0.
    """
    name: str
    bonus: int = 0
    hardness: int = 0
    total_hp: int = 0


class ArmorMixin:

    def get_armor(self) -> Armor:
        """Process the armor information from the character sheet

        Returns:
            Armor: An Armor object
        """
        regex = re.compile(r'armou{0,1}r$')
        armor_string = next((i for i in self.data.keys() if regex.match(i)), None)
        if not armor_string:
            logging.fatal("Character sheet must have an armor/armour section!")
            sys.exit(2)
        if not (data := self.data.get(armor_string)):
            data = dict()

        dexterity = self.stats.get_modifier("dexterity")
        if (cap := data.get("dex_cap", None)) != None:
            dexterity = min(dexterity, cap)

        if (keywords := data.get("keywords", list())) == None:
            keywords = list()

        keywords = self.process_keywords(keywords)

        return Armor(
            ac_bonus=data.get("ac_bonus", 0),
            bonus=data.get("bonus", 0),
            check_penalty=data.get("check_penalty", 0),
            dex_cap=data.get("dex_cap", None),
            dexterity=dexterity,
            equipped=data.get("equipped", True),
            keywords=list(keywords),
            name=data.get("name") if data.get("name") else "Unarmored",
            potency=data.get("potency", 0),
            proficiency_bonus=self.get_proficiency(data.get("proficiency", "untrained")),
            proficiency=data.get("proficiency", "untrained"),
            strength=data.get("strength", None),
        )

    def get_shield(self) -> Shield:
        """Process the shield information from the character sheet

        Returns:
            Shield: A Shield object
        """
        try:
            data = self.data.get("shield", dict())
        except AttributeError:
            data = dict()

        if not data:
            return Shield(name="No Shield")

        return Shield(
            bonus=data.get("bonus", 0),
            hardness=data.get("hardness", 0),
            name=data.get("name"),
            total_hp=data.get("total_hp", 0),
        )
