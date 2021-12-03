from enum import Enum, auto


class CharacterClass(str, Enum):
    WARRIOR = 'warrior'
    TRICKSTER = 'trickster'
    SAGE = 'sage'
    ENCHANTER = 'enchanter'
    MONSTER = 'monster'


class Spell(str, Enum):
    ...


class Attribute(str, Enum):
    XP = 'xp'
    FIGHTTING_PROWESS = 'fighting_prowess' 
    PSYCHIC_ABILITY = 'psychic_ability' 
    AWARENESS = 'awareness' 
    ENDURANCE = 'endurance'
    DAMAGE = 'damage'

class StatusEffects(str, Enum): 
    ... 


class Square(Enum): 
    GRID = auto()
    OBSTACLE = auto()
    PARTIAL = auto() 
    FLEE = auto()