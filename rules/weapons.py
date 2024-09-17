import math
from dataclasses import dataclass
from typing import Generator, Iterable, Optional

from rules.helpers import fix_number


@dataclass
class Weapon:
    """A single weapon/attack generated from the character sheet info.

    Attributes:
        name (str): The name of the weapon/attack.
        keywords (str | Iterable[str]): The keywords associated with the weapon/attack.
        actions (str, optional): The number of actions the attack needs. Defaults to None.
        ammo (int): The amount of ammo the weapon has. Defaults to 0.
        attack_bonus (int): Any miscellaneous modifiers to the attack bonus. Defaults to 0.
        attack_stat_mod (int): The modifier for the attack bonus. Defaults to 0.
        attack_stat (str, optional): The statistic to use when calculating the attack modifiers. Defaults to None.
        damage_bonus (int): Any miscellaneous modifiers to the attack damage. Defaults to 0.
        damage_die_quantity (int): The number of dice to roll for damage for the base weapon. Defaults to 1.
        damage_die_size (int): The number of faces each die has for damage. Defaults to 0.
        damage_stat_mod (int): The modifier for the damage bonus. Defaults to 0.
        damage_stat (int, optional): The statistic to use when calculating the damage. Defaults to None.
        damage_type (str): The damage type(s) of the weapon/attack. Defaults to "slashing".
        dexterity (int): The character's dexterity modifier. Defaults to 0.
        notes (str, optional): Any notes associated with the weapon/attack formatted in Markdown. Default is None.
        potency (int): The bonus added to attacks from potency runes. Defaults to 0.
        proficiency_bonus (int): The proficiency bonus of the weapon/attack. Defaults to 0.
        proficiency (str): The proficiency level of the weapon/attack. Defaults to "untrained".
        source (str): The source of the weapon/attack information in PF2E source books. Defaults to "Unknown".
        strength (int): The character's strength modifier. Defaults to 0.
        striking (int): The number of dice added to the weapon damage due to striking runes. Defaults to 0.
        weapon_type (str): The weapon/attack type (e.g. melee, spell). Defaults to "melee".
    """
    name: str
    keywords: str | Iterable[str]
    actions: Optional[str] = None
    ammo: int = 0
    attack_bonus: int = 0
    attack_stat_mod: int = 0
    attack_stat: Optional[str] = None
    damage_bonus: int = 0
    damage_die_quantity: int = 1
    damage_die_size: int = 0
    damage_stat_mod: int = 0
    damage_stat: Optional[str] = None
    damage_type: str = "slashing"
    dexterity: int = 0
    notes: Optional[str] = None
    potency: int = 0
    proficiency_bonus: int = 0
    proficiency: str = "untrained"
    source: str = "Unknown"
    strength: int = 0
    striking: int = 0
    weapon_type: str = "melee"

    @property
    def get_damage(self) -> str:
        """Generate the damage dealt (e.g. 1d8+3) for the weapon on a successful attack.

        Returns:
            str: The damage string (e.g. 1d8+3).
        """
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
    def get_attacks(self) -> str:
        """Generate the attack bonus progression for the weapon.

        Returns:
            str: The attack progression for the weapon (e.g. '+8/+3/-2')
        """
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

    def process_weapons(self) -> Generator[Weapon, None, None]:
        """Process all of the weapon/attack information in the PF2E character sheet.

        Yields:
            Generator[Weapon, None, None]: A generator with all the weapon/attack information.
        """
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
