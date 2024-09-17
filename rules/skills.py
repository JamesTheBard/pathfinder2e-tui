from dataclasses import dataclass
from typing import Generator

from box import Box

from rules.data import armor_penalty, skill_list


@dataclass
class Skill:
    """Holds all of the information associated with a character skill

    Attributes:
        name (str): The name of the skill.
        bonus (int): The miscellaneous bonus of the skill from items, etc. Defaults to 0.
        check_penalty (int): The armor check penalty of the skill. Defaults to 0.
        modifier (int): The stat modifier of the skill. Defaults to 0.
        proficiency_bonus (int): The proficiency bonus of the skill. Defaults to 0.
        proficiency (str): The proficiency level of the skill. Defaults to "untrained".
        stat (str): The stat associated with the skill. Defaults to "strength".
    """
    name: str
    bonus: int = 0
    check_penalty: int = 0
    modifier: int = 0
    proficiency_bonus: int = 0
    proficiency: str = "untrained"
    stat: int = "strength"

    @property
    def total(self) -> int:
        """Calculate the total skill bonus/penalty for the skill

        Returns:
            int: The total skill bonus/penalty
        """
        return self.modifier + self.proficiency_bonus + self.bonus + self.check_penalty


class SkillsMixin:

    def find_skill(self, skill: str) -> Box:
        """Try to find a skill given the skill name in the character sheet info and return it, or an empty
        dict if it cannot.

        Args:
            skill (str): The name of the skill

        Returns:
            Box: The raw skill information of the character sheet, or an empty dict if not found
        """
        try:
            for s, d in self.data.skills.items():
                if s.casefold() == skill.casefold():
                    return d
        except AttributeError:
            pass

        return Box()

    def calculate_skill(self, skill: str) -> Skill:
        """Calculate all of the skill information given a skill name

        Args:
            skill (str): The name of the skill

        Returns:
            Skill: The Skill object with all of the skill information
        """
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

        result.proficiency = data.get("proficiency", "untrained")
        result.proficiency_bonus = self.get_proficiency(result.proficiency)
        result.stat = data.get("stat", False) or skill_list[skill]
        result.modifier = self.stats.get_modifier(result.stat, dexterity)
        result.bonus = data.get("bonus", 0)

        return result

    def process_skills(self) -> Generator[Skill, None, None]:
        """Process all of the skills from the character sheet raw data

        Yields:
            Generator[Skill, None, None]: All of the skill information from the character sheet
        """
        try:
            defined_skills = [i.casefold() for i in self.data.skills.keys()]
        except AttributeError:
            defined_skills = list()

        skills = sorted(list(set(defined_skills).union(skill_list.keys())))

        for skill in skills:
            yield self.calculate_skill(skill)
