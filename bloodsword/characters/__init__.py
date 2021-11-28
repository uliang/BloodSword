from __future__ import annotations

from abc import ABC
from collections import deque
from ..protocols import DescriptorList


class Character(ABC):
    """
    Subclass Character to create playable character types. Each attribute
    should be declared as a class variable with the Attribute descriptor.
    """

    def __init__(self, name: str, rank: int = 2):
        self.name = name
        self.items_carried = deque([], maxlen=10)

        for attrib in self.descriptors:
            attrib.init(self, rank=rank)

    def store_item(self, item) -> None:
        try:
            self.items_carried.insert(0, item)
        except IndexError as exec:
            ...
            # TODO implement send items full signal

    def remove_item(self, item) -> None:
        self.items_carried.remove(item)

    def __str__(self: DescriptorList) -> str:
        s = ' '.join("{}={}".format(str(attrib), getattr(self, attrib.private_name))
                     for attrib in self.descriptors if str(attrib))
        return f"<Name:{self.name} {s}>"
