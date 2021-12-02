from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from .enumeration import Spell, CharacterClass, Attribute


class Position(ABC):
    ...


@dataclass
class Character(ABC):
    """
    Subclass this abstract class to implement generic rules for all characters. 
    Special rules for each character type are implemented by injecting character
    type specific behaviors using the Builder class as supervised by the Supervisor
    class. 

    .. py:attribute:: rank
        :type: int 
        :value: 2 

        The starting power level of the character. 
    """
    rank: int = field(default=2)

    @abstractmethod
    def move(self, to: Position) -> None:
        """Implement this method to "move" a character. Updating a character's :py:class:`Position <bloodsword.abstract.Position>` only it is an
        allowed movement on the "current" tactical board."""

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
    @abstractmethod
    def build(self, builder: Builder) -> None:
        ...


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
