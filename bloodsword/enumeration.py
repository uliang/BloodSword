from enum import Enum


class CharacterClass(str, Enum):
    WARRIOR = 'warrior'
    TRICKSTER = 'trickster'
    SAGE = 'sage'
    ENCHANTER = 'enchanter'


class Spell(str, Enum):
    ...


class Attribute(str, Enum):
    ...
