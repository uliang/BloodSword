from __future__ import annotations

from abc import ABC, abstractclassmethod, abstractmethod
from dataclasses import dataclass, field
from importlib import import_module
from typing import Any, List, Optional
from math import floor

from .enumeration import Attribute, CharacterClass, Spell, StatusEffects
from .geometry import Position, TacticalMap


@dataclass
class Dice(ABC):
    """
    Subclass to provide logic for Dice object.
    """
    _n: int
    _n_faces: int
    _modifier: Optional[int] = None

    @abstractclassmethod
    def from_string(cls, notation: str) -> Dice:
        """
        :param str notation: Die notation in XdY+Z. 
        :returns: Instance of Dice. 
        :rtype: Dice

        Factory function to create dice object from die notation. 
        """

    @abstractmethod
    def roll(self) -> Score:
        """
        Roll dice and obtain result as a Score object. 
        """


@dataclass(frozen=True, eq=True, order=True)
class Rank(ABC):
    """
    Value object for representing the power level of character, current XP and
    whether character should advance in rank.
    """
    _rank: int = field(compare=True)
    _xp: int = field(compare=False)
    _breakpoint: int = field(compare=False)

    @property
    def rank(self) -> int:
        """
        :returns: Power level of character.
        :rtype: int
        """
        return self._rank

    def __repr__(self) -> str:
        return repr(self._rank)

    @abstractmethod
    def should_advance(self, with_xp: int) -> bool:
        """
        :param int with_xp: Amount of additional xp awarded.
        :returns: True if new rank is attained, False otherwise.
        :rtype: bool

        Implement logic to test whether a new rank is attained. ::

            >>> r = Rank(2, 250, 499)
            >>> r.should_advance(300)
            True
            >>> r.should_advance(200)
            False
        """


@dataclass(frozen=True, eq=True, order=True)
class Score(ABC):
    """
    Subclass this abstract class to implement rules for attribute values.
    E.g., the fact that endurance cannot exceed it's initial value. 

    Score attempts to emulate numeric types. ::

        >>> x = Score(7,7)
        >>> x + Score(5)
        12
        >>> x - Score(1)
        6
        >>> x*2
        14
        >>> x/3
        2
    """
    _value: int = field(compare=True)
    _initial_value: Optional[int] = field(compare=False, default=None)

    def __repr__(self) -> str:
        return repr(self._value)

    def __add__(self, value: Score):
        a = self._increment(value)
        return Score(a, self._initial_value)

    def __sub__(self, value: Score):
        return Score(max(0, self._value - value._value), self._initial_value)

    def __mul__(self, value: int):
        return Score(self._data*value, self._initial_value)

    def __div__(self, value: int):
        """
        Results are always rounded down. 
        """
        return Score(floor(self._value/value), self._initial_value)

    @abstractmethod
    def _increment(self, value: Score) -> int:
        """
        Override this method to implement special rules for incrementing the
        attribute. 
        """


@dataclass
class Character(ABC):
    """
    Subclass this abstract class to implement generic rules for all characters.  
    """
    _fighting_prowess: Score
    _psychic_ability: Score
    _awareness: Score
    _endurance: Score
    _rank: Rank
    _damage: Dice

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
class AdvDataProvider(ABC):
    """
    Factory to provide attribute scores and other data for a character
    of rank :py:attr:`provide_for_rank`. 

    Subclass to provide implementation importing character advancement data from
    a particular source (e.g. database, `json`, `xml`, `toml`, `yaml`, etc...).  

    It is intended to be used in the following way, :: 

        >>> class CharacterAdvDataProviderFromJSON(CharacterAdvDataProvider)
        ...     # logic for reading from a json file here
        >>> provider = CharacterAdvDataProviderFromJSON('./data/sageAdvancement.json', 2)
        >>> provider[Attribute.FIGHTING_PROWESS]
        7

    :param str location_of_adv_data: Location of advancement data. Could be a database connection string, path to a json file.
    :param provide_for_rank: Power level of character. 
    :type provide_for_rank: int or None. 

    If None is provided for :py:attr:`provide_for_rank`, it is assumed that attribute level is available only for a default level. 
    """
    location_of_adv_data: str
    provide_for_rank: Optional[int] = None

    @abstractmethod
    def __getitem__(self, key: Attribute) -> Any:
        ...


@dataclass
class Factory(ABC):
    """
    Subclass this abstract class to provide implementation for creating
    behavior objects for each particular character type.

    :param AdvDataProvider advancement_data: Instance of provider for Advancement Data. 
    """
    advancement_data: AdvDataProvider

    _character: Optional[Character] = field(init=False, default=None)

    @abstractmethod
    def _initialize(self) -> None:
        """
        Override to initialize character instance.
        """

    @abstractmethod
    def _init_equipment(self) -> None:
        """
        Override this method to implement specific equipment for a character. 
        """

    @abstractmethod
    def _learn_special_abilities(self) -> None:
        """
        Override this method to implement special abilities for a character.
        """

    @abstractmethod
    def _learn_spells(self) -> None:
        """
        Override this method to implement spells for Enchanter class. For 
        all other classes, this operation is a no-op. 
        """

    def _create_character(self) -> None:
        self._initialize()
        self._init_equipment()
        self._learn_special_abilities()
        self._learn_spells()

    def get_character(self) -> Character:
        """
        Returns a Character instance."""
        self._create_character()
        return self._character
