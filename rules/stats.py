import math
from dataclasses import dataclass
from typing import Generator, Iterable, Optional

from box.exceptions import BoxKeyError

from rules.data import saves_list


@dataclass
class Stats:
    """The character statistics from the Pathfinder character sheet

    Attributes:
        strength (int): The strength value (not modifier) of the character. Defaults to 10.
        dexterity (int): The dexterity value (not modifier) of the character. Defaults to 10.
        constitution (int): The constitution value (not modifier) of the character. Defaults to 10.
        intelligence (int): The intelligence value (not modifier) of the character. Defaults to 10.
        wisdom (int): The wisdom value (not modifier) of the character.  Defaults to 10.
        charisma (int): The charisma value (not modifier) of the character.  Defaults to 10.
    """
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10

    def get_modifier(self, stat: str, dex_cap: int = None) -> int:
        """Get the modifier for a given stat.

        Args:
            stat (str): The statistic to get.
            dex_cap (int, optional): The dexterity cap to apply. Defaults to None.

        Returns:
            int: The modifier for the statistic.
        """
        stat = stat.casefold()
        if stat not in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
            return -20
        modifier = math.floor((getattr(self, stat) - 10) / 2)
        if dex_cap is not None and stat == "dexterity":
            return min(dex_cap, modifier)
        return modifier


@dataclass
class Save:
    """The character saves and perception information from the character sheet

    Attributes:
        name (str): The name of the save.
        bonus (int): The misc bonus applied to the save. Defaults to 0.
        item_bonus (int): The item bonus applied to the save. Defaults to 0.
        proficiency_bonus (int): The proficiency bonus applied to the save. Defaults to 0.
        proficiency (str): The proficiency level of the save. Defaults to "untrained".
        stat (str): The stat associated with the save. Defaults to "strength".
    """
    name: str
    bonus: int = 0
    item_bonus: int = 0
    modifier: int = 0
    proficiency_bonus: int = 0
    proficiency: str = "untrained"
    stat: str = "strength"

    @property
    def total(self) -> int:
        """Return the total save bonus/penalty.

        Returns:
            int: The total save bonus/penalty
        """
        return sum((
            self.modifier,
            self.proficiency_bonus,
            self.item_bonus,
            self.bonus,
        ))


class StatsMixin:

    def process_stats(self) -> Stats:
        """Process all of the statistics from the character data file.

        Returns:
            Stats: The Stats object with all the statistics information.
        """
        stats = Stats()
        for stat, value in self.data.stats.items():
            setattr(stats, stat, value)
        return stats


class SavesMixin:

    def process_saves(self) -> Generator[Save, None, None]:
        """Process all of the saves from the character data file.

        Yields:
            Iterator[Save]: An iterator of all the Saves.
        """
        dexterity = self.stats.get_modifier("dexterity")

        for save, stat in saves_list.items():
            try:
                data = self.data.saves.get(save, dict())
            except (AttributeError, BoxKeyError):
                data = dict()

            data = data if data else dict()

            result = Save(name=save.title())
            result.stat = stat
            result.modifier = self.stats.get_modifier(stat, dexterity)
            result.item_bonus = data.get("item_bonus", 0)
            result.bonus = data.get("bonus", 0)
            result.proficiency_bonus = self.get_proficiency(data.get("proficiency", "untrained"))
            result.proficiency = data.get("proficiency", "untrained")

            yield result


@dataclass
class Names:
    """The names and other miscellaneous character information from the character data.

    Attributes:
        ancestry (str): The ancestry of the character.
        background (str): The background of the character.
        character_class (str): The class of the character.
        character_level (int): The level of the character.
        heritage (str): The heritage of the character.
        languages (str | Iterable[str]): The languages known by the character.
        name (str): The name of the character.
        player (str): The name of the player.
        diety (str, optional): The diety worshipped by the character. Defaults to None.
        speed_bonus (int): The speed bonus applied to the character. Defaults to 0.
        speed (int): The speed of the character. Defaults to 25.
    """
    ancestry: str
    background: str
    character_class: str
    character_level: int
    heritage: str
    languages: str | Iterable[str]
    name: str
    player: str
    diety: Optional[str] = None
    speed_bonus: int = 0
    speed: int = 25


class NamesMixin:

    def process_names(self) -> Names:
        """Process the 'names' information from the character sheet.

        Returns:
            Names: A Names object with all the random character information.
        """
        data = self.data.character
        results = Names(
            ancestry=data.ancestry,
            background=data.background,
            character_class=data["class"],
            character_level=data.level,
            heritage=data.heritage,
            languages=data.languages,
            name=data.name,
            player=data.player,
        )

        optional = ["diety", "speed", "speed_bonus"]
        for i in optional:
            try:
                setattr(results, i, data[i])
            except KeyError:
                pass

        return results


@dataclass
class HitPoints:
    """The HP information from the character sheet info.

    Attributes:
        ancestry_hp (int): The number of HP granted from the character ancestry.
        class_hp (int): The number of HP granted per level from the character class.
        constitution (int): The constitution modifier. Defaults to 0.
        fast_recovery (bool): Whether the character has the Fast Recovery feat. Defaults to False.
        level (int): The level of the character. Defaults to 0.
        misc (int): Miscellaneous bonuses to HP. Defaults to 0.
        toughness (bool): Whether the character has the Toughness feat. Defaults to False.
    """
    ancestry_hp: int
    class_hp: int
    constitution: int = 0
    fast_recovery: bool = False
    level: int = 0
    misc: int = 0
    toughness: bool = False

    @property
    def total(self) -> int:
        """Calculate the total number of HP the character has.

        Returns:
            int: _description_
        """
        return (self.class_hp + self.constitution + self.toughness) * self.level + self.ancestry_hp + self.misc

    @property
    def rest(self) -> int:
        """Calculate the number of HP gained during a rest.

        Returns:
            int: The number of HP gained during a rest
        """
        return max(self.constitution, 1) * self.level * (self.fast_recovery + 1)


class HitPointsMixin:

    def process_hit_points(self) -> HitPoints:
        """Process all of the HP information from the character sheet info.

        Returns:
            HitPoints: The HP information from the character sheet.
        """
        data = self.data.hit_points
        results = HitPoints(
            class_hp=data["class"],
            ancestry_hp=data.ancestry,
            level=self.character.character_level,
            constitution=self.stats.get_modifier("constitution"),
        )

        optional = ["toughness", "ancestry", "misc"]
        for i in optional:
            try:
                setattr(results, i, data[i])
            except KeyError:
                pass

        return results
