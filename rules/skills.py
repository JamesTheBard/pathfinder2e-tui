from dataclasses import dataclass
from typing import Iterator

from rules.data import armor_penalty, skill_list


@dataclass
class Skill:
    name: str
    stat: int = 0
    modifier: int = 0
    proficiency: str = ""
    proficiency_bonus: int = 0
    bonus: int = 0
    check_penalty: int = 0

    @property
    def total(self) -> int:
        return self.modifier + self.proficiency_bonus + self.bonus + self.check_penalty

    @property
    def data(self) -> tuple[str, str, str, int, int, int, int]:
        return (
            self.name,
            self.total,
            self.stat,
            self.modifier,
            self.proficiency,
            self.proficiency_bonus,
            self.bonus,
            self.check_penalty,
        )


class SkillsMixin:

    def find_skill(self, skill):
        try:
            for s, d in self.data.skills.items():
                if s.casefold() == skill.casefold():
                    return d
        except AttributeError:
            pass

        return dict()

    def calculate_skill(self, skill: str) -> Skill:
        skill = skill.casefold()
        result = Skill(name=skill.title())

        data = self.find_skill(skill)

        strength = self.stats.get_modifier("strength")
        dexterity = self.stats.get_modifier("dexterity")

        if skill.startswith("lore"):
            data["stat"] = "intelligence"

        if self.armor.check_penalty:
            if self.armor.strength > strength and skill in armor_penalty:
                result.check_penalty = self.armor.check_penalty
            # if self.armor.dex_cap != None:
            #     dexterity = self.armor.dex_cap

        result.proficiency = data.get("proficiency", "untrained")
        result.proficiency_bonus = self.get_proficiency(result.proficiency)
        result.stat = data.get("stat", False) or skill_list[skill]
        result.modifier = self.stats.get_modifier(result.stat, dexterity)
        result.bonus = data.get("bonus", 0)

        return result

    def process_skills(self) -> Iterator[Skill]:
        try:
            defined_skills = [i.casefold() for i in self.data.skills.keys()]
        except AttributeError:
            defined_skills = list()

        skills = sorted(list(set(defined_skills).union(skill_list.keys())))

        for skill in skills:
            yield self.calculate_skill(skill)
