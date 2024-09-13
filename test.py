import yaml
from box import Box
from rules.character_sheet import CharacterSheet
from rules.skills import skill_headers

a = CharacterSheet()
a.load_character_sheet(yaml_file='info.yaml')
# a.refresh()

print(a.stats)

print()
[print(i, i.total) for i in a.skills]

print()
[print(i, i.total) for i in a.saves]

print()
print(a.armor, a.armor.total)

print()
print(a.shield)

print()
[print(i, i.get_attacks, i.get_damage) for i in a.weapons]