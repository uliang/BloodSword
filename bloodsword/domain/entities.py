from abc import ABC, abstractmethod, abstractclassmethod
from dataclasses import dataclass
from typing import List

from .values import Dice, Position, Rank, Score


@dataclass
class Attributes(ABC):
    fighting_prowess: Score
    psychic_ability: Score
    awareness: Score
    endurance: Score
    rank: Rank
    damage: Dice



