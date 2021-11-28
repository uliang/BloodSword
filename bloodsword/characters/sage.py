from ..descriptors.armour import Armour
from ..descriptors.attributes import Attribute
from ..base import Character


class Sage(Character):
    fighting_prowess = Attribute(verbose_name="Fighting Prowess",
                                 rank_attributes=[7, 7, 7, 7, 7, 7, 8])
    psychic_ability = Attribute(verbose_name="Psychic Ability",
                                rank_attributes=[7, 7, 8, 8, 8, 8, 8])
    awareness = Attribute(verbose_name="Awareness",
                          rank_attributes=[6, 6, 7, 7, 7, 7, 7])
    endurance = Attribute(verbose_name="Endurance", has_max_value=True,
                          rank_attributes=[10, 15, 20, 25, 30, 35, 40])
    armour = Armour("ringmail", damage_reduction=2)