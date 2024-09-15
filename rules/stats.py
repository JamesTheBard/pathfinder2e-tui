import math
from dataclasses import dataclass
from typing import Iterator, Optional

from rich.text import Text

from rules.data import prof_map, saves_list, stats_shorthand
from rules.helpers import fix_number


@dataclass
class Stats:
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10

    @property
    def data(self) -> Iterator[tuple[str, int, int]]:
        for stat in stats_shorthand.keys():
            yield (
                stat.title(),
                getattr(self, stat),
                self.get_modifier(stat)
            )

    @property
    def data_short(self) -> Iterator[tuple[str, int, int]]:
        for stat, short in stats_shorthand.items():
            yield (short.title(), getattr(self, stat), fix_number(self.get_modifier(stat)))

    def get_modifier(self, stat, dex_cap=None) -> int:
        if dex_cap is not None and stat == "dexterity":
            return dex_cap
        return math.floor((getattr(self, stat) - 10) / 2)


@dataclass
class Save:
    name: str
    stat: str = ""
    modifier: int = 0
    proficiency: int = 0
    proficiency_bonus: int = 0
    item_bonus: int = 0
    bonus: int = 0

    @property
    def data(self) -> tuple[str, int, str, int, int, int, int]:
        return (
            self.name.title(),
            self.total,
            self.stat,
            self.modifier,
            self.proficiency,
            self.proficiency_bonus,
            self.item_bonus,
            self.bonus,
        )

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

        # if self.armor.dex_cap != None:
        #     dexterity = self.armor.dex_cap

        for save, stat in saves_list.items():
            data = self.data.saves.get(save, dict())
            data = data if data else dict()

            result = Save(name=save.title())
            result.stat = stats_shorthand[stat]
            result.modifier = self.stats.get_modifier(stat, dexterity)
            result.item_bonus = data.get("item_bonus", 0)
            result.bonus = data.get("bonus", 0)
            result.proficiency_bonus = self.get_proficiency(data.get("proficiency", "untrained"))
            result.proficiency = data.get("proficiency", "untrained")

            yield result


@dataclass
class Names:
    name: str
    player: str
    ancestry: str
    heritage: str
    background: str
    languages: list
    classes: list
    diety: Optional[str] = None


class NamesMixin:

    def process_names(self):
        data = self.data.character
        results = Names(
            name=data.name,
            player=data.player,
            ancestry=data.ancestry,
            heritage=data.heritage,
            background=data.background,
            languages=data.languages,
            classes=data.classes,
        )

        optional = ["diety"]
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
    toughness: bool = False
    fast_recovery: bool = False
    misc: int = 0
    level: int = 0
    constitution: int = 0

    @property
    def total(self):
        return (self.class_hp + self.constitution + self.toughness) * self.level + self.ancestry_hp + self.misc

    @property
    def rest(self):
        return max(self.constitution, 1) * self.level * (self.fast_recovery + 1)


class HitPointsMixin:

    def process_hit_points(self) -> HitPoints:
        data = self.data.hit_points
        results = HitPoints(
            class_hp=data["class"],
            ancestry_hp=data.ancestry,
            level=self.level,
            constitution=self.stats.get_modifier("constitution"),
        )

        optional = ["toughness", "ancestry", "misc"]
        for i in optional:
            try:
                setattr(results, i, data[i])
            except KeyError:
                pass

        return results
