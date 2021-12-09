from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

from .values import Score, Rank
from .entities import Attributes

@dataclass
class Advancement(ABC):
    """
    Advancement class aggregates character Attribute list and implements 
    advancement behavior.
    """
    _data: List[Attributes] = field(default_factory=list)

    @abstractmethod
    def advance_by_rank(self, rank: Rank) -> Attributes:
        """
        Override to implement logic to search list for Attributes with
        matching Rank and return.
        """

    @abstractmethod
    def advance_by_xp(self, xp: Score) -> Attributes:
        """
        Override to implement logic to search list for Attributes with largest
        rank breakpoint smaller than `xp`
        """
