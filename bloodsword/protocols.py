from __future__ import annotations

from typing import Protocol, ClassVar


class Descriptor(Protocol):
    def __init__(self):
        self.private_name: str

    def __get__(self, instance):
        ...

    def __set__(self, instance, type_):
        ...

    def init(self, instance, **kwargs):
        ...


class DescriptorList(Protocol):
    descriptors: ClassVar[list[Descriptor]]


class Storage(Protocol):
    def store_item(self, item) -> None:
        ...

    def remove_item(self, item) -> None:
        ...
