from __future__ import annotations

from abc import ABC
import typing
from collections import deque


@typing.runtime_checkable
class Progressable(typing.Protocol):
    def get_rank_attribute_value(self, rank: int) -> int:
        pass


@typing.runtime_checkable
class Initializable(typing.Protocol):
    def initialize_with(self, instance, value) -> None:
        pass

    def get_initial_value(self, instance) -> int:
        pass


@typing.runtime_checkable
class Equipable(typing.Protocol):
    def equip_on(self, instance):
        pass


class Character(ABC):
    """
    Subclass Character to create playable character types. Each attribute
    should be declared as a class variable with the Attribute descriptor.
    """

    def __init__(self, name: str, **initial_attribute_values):
        self.name = name
        self.items_carried = deque([], maxlen=10)

        for name, var in vars(self.__class__).items():
            if isinstance(var, Equipable):
                var.equip_on(self)
            if isinstance(var, Initializable):
                var.initialize_with(self, initial_attribute_values[name])

    @classmethod
    def from_rank(cls, name: str, rank: int = 2) -> Character:
        kwargs = {k: v.get_rank_attribute_value(
            rank) for k, v in vars(cls).items() if isinstance(v, Progressable)}
        return cls(name, **kwargs)

    def store_item(self, item) -> None:
        try:
            self.items_carried.insert(0, item)
        except IndexError as exec:
            ...
            # TODO implement send items full signal

    def remove_item(self, item) -> None:
        self.items_carried.remove(item)

    def __str__(self) -> str:
        s = ' '.join('{:s}={:d}'.format(*attrib.get_initial_value(self)) for attrib in vars(
            self.__class__).values() if isinstance(attrib, Initializable))
        return f"<Name:{self.name} {s}>"
