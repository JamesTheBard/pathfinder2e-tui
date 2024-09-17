import math
from dataclasses import dataclass
from typing import Iterator, Optional

from box.exceptions import BoxKeyError

from rules.data import saves_list


@dataclass
class Stats:
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10

    def get_modifier(self, stat, dex_cap: int = None) -> int:
        modifier = math.floor((getattr(self, stat) - 10) / 2)
        if dex_cap is not None and stat == "dexterity":
            return min(dex_cap, modifier)
        return modifier


@dataclass
class Save:
    name: str
    bonus: int = 0
    item_bonus: int = 0
    modifier: int = 0
    proficiency_bonus: int = 0
    proficiency: int = 0
    stat: str = ""

    @property
    def total(self) -> int:
        return sum((
            self.modifier,
            self.proficiency_bonus,
            self.item_bonus,
            self.bonus,
        ))


class StatsMixin:

    def process_stats(self) -> Stats:
        stats = Stats()
        for stat, value in self.data.stats.items():
            setattr(stats, stat, value)
        return stats


class SavesMixin:

    def process_saves(self) -> Iterator[Save]:
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
    ancestry: str
    background: str
    classes: list
    heritage: str
    languages: list
    name: str
    player: str
    diety: Optional[str] = None
    speed_bonus: int = 0
    speed: int = 25


class NamesMixin:

    def process_names(self) -> Names:
        data = self.data.character
        results = Names(
            name=data.name,
            player=data.player,
            ancestry=data.ancestry,
            heritage=data.heritage,
            background=data.background,
            languages=data.languages,
            classes=f"{data["class"]} {data.level}",
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
    class_hp: int
    ancestry_hp: int
    constitution: int = 0
    fast_recovery: bool = False
    level: int = 0
    misc: int = 0
    toughness: bool = False

    @property
    def total(self) -> int:
        return (self.class_hp + self.constitution + self.toughness) * self.level + self.ancestry_hp + self.misc

    @property
    def rest(self) -> int:
        return max(self.constitution, 1) * self.level * (self.fast_recovery + 1)


class HitPointsMixin:

    def process_hit_points(self) -> HitPoints:
        data = self.data.hit_points
        results = HitPoints(
            class_hp=data["class"],
            ancestry_hp=data.ancestry,
            level=self.character_level,
            constitution=self.stats.get_modifier("constitution"),
        )

        optional = ["toughness", "ancestry", "misc"]
        for i in optional:
            try:
                setattr(results, i, data[i])
            except KeyError:
                pass

        return results
