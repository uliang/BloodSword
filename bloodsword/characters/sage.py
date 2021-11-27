from ..descriptors.attributes import Attribute
from ..base import Character


class Sage(Character):
    fighting_prowess = Attribute()
    psychic_ability = Attribute()
    awareness = Attribute()
    endurance = Attribute(has_max_value=True)
