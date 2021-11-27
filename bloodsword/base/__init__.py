from __future__ import annotations

from typing import Tuple


class Character:
    def __init__(self, name, fp, pa, a, e):
        self.name = name
        self.fighting_prowess = fp
        self.psychic_ability = pa
        self.awareness = a
        self.endurance = e

    @classmethod
    def from_tuple(cls, name, tup: Tuple[int, int, int, int]) -> Character:
        return cls(name, *tup)

    def __str__(self) -> str:
        return f"Character(class:{self.name} Fighting Prowess={self.fighting_prowess} Psychic Ability={self.psychic_ability} Awareness={self.awareness} Endurance={self.endurance})"
