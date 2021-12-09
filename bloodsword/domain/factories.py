from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional
from .aggregates import Character


@dataclass
class CharacterFactory(ABC):
    """
    Subclass this abstract class to provide implementation for creating
    behavior objects for each particular character type.
    """
    _character: Optional[Character] = field(init=False, default=None)

    @abstractmethod
    def _initialize(self) -> None:
        """
        Override to implement logic to create a new character instance.
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
