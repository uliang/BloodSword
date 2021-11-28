from __future__ import annotations

from dataclasses import dataclass

from ..protocols import Storage, DescriptorList


@dataclass
class Armour:
    name: str
    damage_reduction: int

    def init(self, instance: Storage, **kwargs):
        instance.store_item(self)
        setattr(instance, self.private_name, self)

    def __set_name__(self, owner: DescriptorList, name):
        self.private_name = f"_{name}"
        owner.descriptors.append(self)

    def __get__(self, instance, type_=None):
        return getattr(instance, self.private_name)

    def __set__(self, instance: Storage, value: Armour):
        setattr(instance, self.private_name, value)
        instance.remove_item(self)
        instance.store_item(value)

    def __str__(self) -> str:
        return ''
