from ..base import Character
from ..descriptors.attributes import Attribute

class Warrior(Character): 
    fighting_prowess = Attribute()
    psychic_ability = Attribute()
    awareness = Attribute()
    endurance = Attribute(has_max_value=True)
