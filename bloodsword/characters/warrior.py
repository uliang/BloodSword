from . import Character
from ..descriptors.attributes import Attribute
from ..descriptors.armour import Armour
from ..protocols import Descriptor
from typing import ClassVar

class Warrior(Character):
    fighting_prowess = Attribute(
        verbose_name="Fighting Prowess", rank_attributes=[8, 8, 8, 8, 8, 8, 9])
    psychic_ability = Attribute(
        verbose_name="Psychic Ability", rank_attributes=[6, 6, 6, 6, 6, 6, 7])
    awareness = Attribute(verbose_name="Awareness",
                          rank_attributes=[6, 6, 7, 7, 7, 7, 7])
    endurance = Attribute(verbose_name="Endurance", has_max_value=True,
                          rank_attributes=[12, 18, 24, 30, 36, 42, 48])
    armour = Armour("chainmail", damage_reduction=3)