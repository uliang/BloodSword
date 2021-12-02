from __future__ import annotations

from abc import ABC, abstractclassmethod, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from .enumeration import Spell, CharacterClass, Attribute


@dataclass
class Position:
    """
    Position on a tactical map. 

    We follow the convention where the origin is located at the top left corner
    of the map. 
    """
    x: int = 0
    y: int = 0


@dataclass
class TacticalMap(ABC):
    """
    Abstract class to implement logic for acquiring data of valid sqaures
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

    @abstractclassmethod
    def from_listoflists(cls, diagram: List[List[str]]) -> None:
        """
        Implement parsing logic for string representation of grid. 

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


@dataclass
class Character(ABC):
    """
    Subclass this abstract class to implement generic rules for all characters. 
    Special rules for each character type are implemented by injecting character
    type specific behaviors using the Builder class as supervised by the Supervisor
    class. 

    .. py:attribute:: fighting_prowess
        :type: int
        :value: 0

        A measure of how skilled and powerful a fighter the character is.

    .. py:attribute:: psychic_ability
        :type: int
        :value: 0 

        A measure of resistance to hostile spells and for an Echanter, his or her
        aptitude for magic. 

    .. py:attribute:: awareness
        :type: int 
        :value: 0

        Quickness of thought, dexterity and wits. 

    .. py:attribute:: rank
        :type: int 
        :value: 2 

        The starting power level of the character. 

    .. py:attribute:: xp 
        :type: int 
        :value: 250 

        Initial experience points. 
    """
    fighting_prowess: int = 0
    psychic_ability: int = 0
    awareness: int = 0

    _endurance: int = field(init=False)
    _initial_endurance: int = field(default=None, init=False)
    _current_position: Position = field(init=False, default=(0, 0))

    rank: int = field(default=2)
    xp: int = field(default=250)

    @property
    def endurance(self) -> int:
        """A measure of a character's state of health. It can never go above it's initial
        value."""
        return self._endurance

    @endurance.setter
    def endurance(self, value: int) -> None:
        if self._initial_endurance is None:
            self._endurance = value
            self._initial_endurance = value
            return
        value = min(self._initial_endurance, max(0, value))
        self._endurance = value

    @abstractmethod
    def move(self, to: Position, on: TacticalMap) -> None:
        """
        :param to: Destination coordinate.
        :type to: Position
        :param TacticalMap on: The current tactical map. 
        :rtype: NoneType

        Implement this method to "move" a character. Updating a character's :py:class:`Position <bloodsword.abstract.Position>` 
        only if is an allowed movement on the "current" tactical board.
        """

    @abstractmethod
    def fight(self, target: Character):
        ...

    @abstractmethod
    def defend(self):
        ...

    @abstractmethod
    def shoot(self):
        ...

    @abstractmethod
    def flee(self):
        ...

    @abstractmethod
    def call_a_spell_to_mind(self, spell: Spell):
        ...

    @abstractmethod
    def cast_a_spell_in_mind(self, spell: Spell):
        ...


@dataclass
class CharacterAdvDataProvider(ABC):
    """
    Abstract Factory to provide attribute scores and other data for a character
    of rank `provide_for_rank`. 

    Subclass to provide implementation importing character advancement data from
    a particular source (e.g. database, json, xml, toml, yaml, etc...).  
    """
    provide_for_character_class: CharacterClass
    provide_for_rank: int = field(default=2)

    @abstractmethod
    def __getitem__(self, key: Attribute) -> Any:
        ...


class Supervisor(ABC):
    """
    Concrete supervisors provide concrete implementations for character creation process. 
    """
    @abstractmethod
    def build(self, builder: Builder) -> None:
        """
        Implement logic for injecting particular character rules as behavior instances
        into an initialized character. 
        """


@dataclass
class Builder(ABC):
    """
    Subclass this abstract class to provide implementation for creating
    behavior objects for each particular character type.

    Attributes
    ----------
    character_advancement_data: Requests for character attribute and damage 
        data is delegated to this Provi
    """
    character_advancement_data: CharacterAdvDataProvider
    _character: Character = field(init=False)

    @abstractmethod
    def set_experience_points(self) -> None:
        ...

    @abstractmethod
    def init_attributes(self) -> None:
        ...

    @abstractmethod
    def init_equipment(self) -> None:
        ...

    @abstractmethod
    def learn_special_abilities(self) -> None:
        ...

    @abstractmethod
    def learn_spells(self) -> None:
        ...

    @abstractmethod
    def get_character(self) -> Character:
        ...