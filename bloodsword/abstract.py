from __future__ import annotations

from abc import ABC, abstractclassmethod, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Deque, List, Optional
from math import floor

from .enumeration import Attribute, Spell, StatusEffects
from .geometry import Position, TacticalMap



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
