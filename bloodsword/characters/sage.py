from ..descriptors.attributes import Attribute
from ..base import Character


class Sage(Character):
    fighting_prowess = Attribute(rank_attributes=[7, 7, 7, 7, 7, 7, 8])
    psychic_ability = Attribute(rank_attributes=[7, 7, 8, 8, 8, 8, 8])
    awareness = Attribute(rank_attributes=[6, 6, 7, 7, 7, 7, 7])
    endurance = Attribute(has_max_value=True,
                          rank_attributes=[10, 15, 20, 25, 30, 35, 40])
