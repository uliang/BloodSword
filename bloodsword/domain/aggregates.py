from __future__ import annotations

from abc import ABC, abstractclassmethod, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, List

from .entities import Attributes
from .enumeration import Spell, StatusEffects
from .values import Position


@dataclass
class Character(ABC):
    """
    Subclass this abstract class to implement generic rules for all characters.  
    """
    _attributes: Attributes

    _current_position: Position = field(default=Position(0, 0))
    _status_effects: List[StatusEffects] = field(default_factory=list)
    _items_carried: Deque = field(default=deque([], maxlen=10))

    def __repr__(self) -> str:
        return f"{type(self).__name__}(rank={self.rank})"

    def move(self, to: Position, on: TacticalMap) -> None:
        """
        :param to: Destination coordinate.
        :type to: Position
        :param TacticalMap on: The current tactical map. 
        :rtype: NoneType

        Updates a character's :py:class:`Position <bloodsword.abstract.Position>` 
        only if is an allowed movement on the  tactical board.
        """

    @abstractmethod
    def fight(self, target: Character):
        """
        :param Character target: Target of attack. 
        :rtype: NoneType

        Perform a melee attack action. Character must roll *under* :py:attr:`fighting prowess <fighting_prowess>` in order 
        to score a hit with 2d6 and 3d6 if target is defending. Special modifiers may apply. Character can only attack 
        a target which is adjacent to them. 
        """

    @abstractmethod
    def defend(self):
        """
        Perform the defend action. This makes character harder to hit. The opponent needs to roll on 3d6
        to hit. Modifiers may apply. """

    @abstractmethod
    def shoot(self, target: Character):
        """
        Perform the shoot action. Not all characters may shoot. Shooting is only allowed if equipped with
        bow and a quiver containing at least one arrow and target is not adjacent"""

    @abstractmethod
    def flee(self):
        """
        Flee from combat. Fleeing is allowed if on a :py:class:`fleeing <bloodsword.enumeration.Square>` square
        or adjacent to a character who can flee."""

    @abstractmethod
    def call_a_spell_to_mind(self, spell: Spell):
        """
        Spell must be prepared before casting. A character can call a spell to mind at any time but 
        every spell called to mind reduces :py:attr:`psychic ability <psychic_ability>` by one."""

    @abstractmethod
    def cast_a_spell_in_mind(self, spell: Spell):
        """
        Cast a spell held in mind. To cast, roll 2d6 and add spell complexity level. Spell is cast
        successfully if the player rolls *under* the current :py:attr:`psychic ability <psychic_ability>`
        score. If the casting failed, the same spell may be cast again by reducing roll result by one. 

        The casting roll is reset once a spell is cast successfully."""


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

    @abstractmethod
    def valid_destination(self, destination: Position) -> bool:
        """
        Determines if destination can be moved into
        """
    @abstractmethod
    def compute_nearest(self, pc_positions: List[Position], monster_position: Position) -> Position:
        """
        Determines nearest player character to monster.
        """
