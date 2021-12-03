from __future__ import annotations
from importlib import import_module
from abc import ABC, abstractclassmethod, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional



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

    .. py:attribute:: damage
        :type: str
        :value: '1d6'

        Amount of damage dealt on hit. 

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
    damage: str = '1d6'

    _endurance: int = field(init=False)
    _initial_endurance: Optional[int] = field(default=None, init=False)
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
    of rank :py:attr:`provide_for_rank`. 

    Subclass to provide implementation importing character advancement data from
    a particular source (e.g. database, `json`, `xml`, `toml`, `yaml`, etc...).  

    It is intended to be used in the following way, :: 

        >>> class CharacterAdvDataProviderFromJSON(CharacterAdvDataProvider)
        ...     # logic for reading from a json file here
        >>> provider = CharacterAdvDataProviderFromJSON(CharacterClass.SAGE, 2)
        >>> provider[Attribute.FIGHTING_PROWESS]
        7

    .. py:attribute:: provide_for_character_class
        :type: bloodsword.enumeration.CharacterClass

        Advancement data for character of given :py:class:`type <bloodsword.enumeration.CharacterClass>`

    .. py:attribute:: provide_for_rank
        :type: int 
        :value: 2

        Starting rank when initializing character. 
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

    .. 
    .. py:attribute:: character
        :type: str

        Qualified name of the module containing concrete character. Module should expose a concrete 
        subclass of abstract.Character as Character. 

    .. py:attribute:: character_advancement_data
        :type: str

        Qualified name of the module containing the concrete subclass of CharacterAdvDataProvider. 
        Module should expose the Provider concrete class to be initialized 

    One should initialize a character in the :py:meth:`__post_init__` method on the subclass and 
    save it to the private variable :py:attr:`_character`. 
    """
    character_class: Attribute
    rank: int
    character: str
    character_advancement_data: str

    _character: Character = field(init=False)
    _character_adv_data: CharacterAdvDataProvider = field(init=False)

    def __post_init__(self):
        self._character = import_module(self.character).Character()
        self._character_adv_data = import_module(
            self.character_advancement_data).Provider(self.character_class, self.rank)

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
