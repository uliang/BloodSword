from ..base import Character
from ..descriptors.attributes import Attribute


class Warrior(Character):
    fighting_prowess = Attribute(rank_attributes=[8, 8, 8, 8, 8, 8, 9])
    psychic_ability = Attribute(rank_attributes=[6, 6, 6, 6, 6, 6, 7])
    awareness = Attribute(rank_attributes=[6, 6, 7, 7, 7, 7, 7])
    endurance = Attribute(has_max_value=True,
                          rank_attributes=[12, 18, 24, 30, 36, 42, 48])
