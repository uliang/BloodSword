from __future__ import annotations

from typing import Tuple


    def __init__(self, name: str, fighting_prowess: int, psychic_ability: int, awareness: int, endurance: int):
        self.name = name
        self.fighting_prowess = fighting_prowess
        self.psychic_ability = psychic_ability
        self.awareness = awareness
        self.endurance = endurance

    @classmethod
    def from_tuple(cls, name, tup: Tuple[int, int, int, int]) -> Character:
        return cls(name, *tup)

    def __str__(self) -> str:
        return f"Character(class:{self.name} Fighting Prowess={self.fighting_prowess} Psychic Ability={self.psychic_ability} Awareness={self.awareness} Endurance={self.endurance})"
