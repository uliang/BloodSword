from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .enumeration import Square


@dataclass
class Position:
    """
    Position on a tactical map. 

    We follow the convention where the origin is located at the top left corner
    of the map. 
    """
    x: int = 0
    y: int = 0


    def __repr__(self):
        return repr((self.x, self.y))

