import math
from dataclasses import dataclass
from typing import Optional

from rules.helpers import fix_number


@dataclass
class Weapon:
    name: str
    keywords: list[str]
    damage_type: str = ""
    proficiency: str = "untrained"
    proficiency_bonus: int = 0
    potency: int = 0
    attack_bonus: int = 0
    attack_stat: Optional[str] = None
    attack_stat_mod: int = 0
    damage_stat: Optional[str] = None
    damage_stat_mod: int = 0
    damage_bonus: int = 0
    strength: int = 0
    dexterity: int = 0
    damage_die_size: int = 0
    damage_die_quantity: int = 1
    striking: int = 0
    ammo: int = 0
    weapon_type: str = "melee"
    source: str = "Unknown"
    notes: Optional[str] = None
    actions: Optional[str] = None

    @property
    def get_damage(self):
        damage_bonus = self.damage_bonus

        if self.damage_stat:
            damage_bonus += self.damage_stat_mod
        else:
            if "propulsive" in self.keywords:
                damage_bonus += math.floor(self.strength / 2)
            if self.weapon_type == "melee":
                damage_bonus += self.strength

        dice_number = self.damage_die_quantity + self.striking

        return f"{dice_number}d{self.damage_die_size}{fix_number(damage_bonus, True)}"

    @property
    def get_attacks(self):
        attack_bonus = self.attack_bonus + self.potency + self.proficiency_bonus

        if self.attack_stat != None:
            attack_bonus += self.attack_stat_mod
        elif "finesse" in self.keywords:
            attack_bonus += max(self.dexterity, self.strength)
        elif self.weapon_type == "ranged":
            attack_bonus += self.dexterity
        elif self.weapon_type == "melee":
            attack_bonus += self.strength

        multiattack_penalty = -4 if "agile" in self.keywords else -5
        attacks = [fix_number(attack_bonus + (i * multiattack_penalty), True) for i in range(3)]
        return attacks


class WeaponsMixin:

    def process_weapons(self):
        for weapon_name, data in self.data.weapons.items():
            result = Weapon(name=weapon_name.replace('_', ' ').title(), keywords=list())
            [setattr(result, key, value) for key, value in data.items()]
            result.keywords = self.process_keywords(result.keywords)
            result.strength = self.stats.get_modifier("strength")
            result.dexterity = self.stats.get_modifier("dexterity")
            result.proficiency_bonus = self.get_proficiency(result.proficiency)
            if result.attack_stat:
                result.attack_stat_mod = self.stats.get_modifier(result.attack_stat)
            
            if result.damage_stat:
                result.damage_stat_mod = self.stats.get_modifier(result.damage_stat)

            if result.actions != None:
                result.actions = str(result.actions)

            yield result
