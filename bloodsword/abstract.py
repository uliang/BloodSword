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

    .. py:attribute:: path_to_adv_data
        :type: str

        Path to advancement data. 

    .. py:attribute:: provide_for_rank
        :type: int or None
        :value: None

        Starting rank when initializing character. Not that if None, then the provider assumes 
        that only default attribute data is returned. 
    """
    path_to_adv_data: str
    provide_for_rank: Optional[int] = None

    @abstractmethod
    def __getitem__(self, key: Attribute) -> Any:
        ...


class Factory(ABC):
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

    def __init__(self,
                 character_class: Attribute,
                 rank: int,
                 character: str,
                 advancement_data_provider: Optional[str]
                 ) -> None:
        self._character: Character = import_module(character).Character()
        self._character.rank = rank
        self._character_adv_data: AdvDataProvider = import_module(
            advancement_data_provider).Provider(character_class, rank)

    def _set_experience_points(self) -> None:
        self._character.xp = self._character_adv_data[Attribute.XP]

    def _init_attributes(self) -> None:
        self._character.fighting_prowess = self._character_adv_data[Attribute.FIGHTTING_PROWESS]
        self._character.psychic_ability = self._character_adv_data[Attribute.PSYCHIC_ABILITY]
        self._character.awareness = self._character_adv_data[Attribute.AWARENESS]
        self._character.endurance = self._character_adv_data[Attribute.ENDURANCE]
        self._character.damage = self._character_adv_data[Attribute.DAMAGE]

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
        self._set_experience_points()
        self._init_attributes()
        self._init_equipment()
        self._learn_special_abilities()
        self._learn_spells()

    @abstractmethod
    def get_character(self) -> Character:
        ...
