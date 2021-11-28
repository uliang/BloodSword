from __future__ import annotations

from abc import ABC
import typing


@typing.runtime_checkable
class Progressable(typing.Protocol):
    def get_rank_attribute_value(self, rank: int) -> int:
        pass


class Character(ABC):
    """
    Subclass Character to create playable character types. Each attribute
    should be declared as a class variable with the Attribute descriptor.
    """

    def __init__(self, name: str, fighting_prowess: int, psychic_ability: int, awareness: int, endurance: int):
        self.name = name
        self.fighting_prowess = fighting_prowess
        self.psychic_ability = psychic_ability
        self.awareness = awareness
        self.endurance = endurance

    @classmethod
    def from_rank(cls, name: str, rank: int = 2) -> Character:
        kwargs = {k: v.get_rank_attribute_value(
            rank) for k, v in cls.__dict__.items() if isinstance(v, Progressable)}
        return cls(name, **kwargs)

    def __str__(self) -> str:
        return f"<Name:{self.name} Fighting Prowess={self.fighting_prowess} Psychic Ability={self.psychic_ability} Awareness={self.awareness} Endurance={self.endurance}>"
