from __future__ import annotations
from dataclasses import dataclass
import typing


class Storage(typing.Protocol):
    def store_item(self, item) -> None:
        ...

    def remove_item(self, item) -> None:
        ...


@dataclass
class Armour:
    name: str
    damage_reduction: int

    def equip_on(self, instance: Storage):
        instance.store_item(self)
        setattr(instance, self.private_name, self)

    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, instance, type_=None):
        return getattr(instance, self.private_name)

    def __set__(self, instance: Storage, value: Armour):
        setattr(instance, self.private_name, value)
        instance.remove_item(self)
        instance.store_item(value)
