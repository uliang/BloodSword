from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .enumeration import Square


@dataclass
class TacticalMap:
    """
    Representation of valid sqaures
    which a character can pass through, obstacles and squares which monsters
    but not characters may pass through. 

    .. py:attribute:: grids
        :type: List[Position]

        Players may pass through these squares. 

    .. py:attribute:: obstacles
        :type: List[Position]

        Neither monsters nor players can pass through these squares.

    .. py:attribute:: partial_obstacles
        :type: List[Position]

        Monsters may pass through these squares but not players. 

    .. py:attribute:: flee 
        :type: List[Position] 

        Player may flee only when on this square or is adjacent to a player adjacent or
        on a fleeing square. 
    """
    grids: List[Position]
    obstacles: List[Position]
    partial_obstacles: List[Position]
    flee: List[Position]

    def from_listoflists(cls, diagram: List[List[str]]) -> None:
        """
        Parsing logic for string representation of grid. 

        For example, ::

            >>> diagram = [
                    ['o', 'o'], 
                    ['*', 'x'],
                    ['*', 'f']
                ]
            >>> map = TacticalMap.from_listoflists(diagram)
            >>> map.grids 
            [(0,0), (0, 1)]
            >>> map.obstacles
            [(1,1)]
            >>> map.partial_obstacles
            [(1,0), (2,0)]   
            >>> map.flee
            [(2, 1)]
        """

    def valid_destination(self, destination: Position) -> bool:
        """
        Determines if destination can be moved into
        """

    def compute_nearest(self, pc_positions: List[Position], monster_position: Position) -> Position:
        """
        Determines nearest player character to monster.
        """
