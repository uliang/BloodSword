from dataclasses import dataclass, field
from typing import List


@dataclass
class Attribute:
    has_max_value: bool = False
    min_value: int = 0
    rank_attributes: List[int] = field(default_factory=list)

    def __set_name__(self, owner, name):
        self.private_name = '_' + name
        self.initial_name = f'_initial_{name}_value'

    def __get__(self, instance, type_=None):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        value = max(self.min_value, value)
        if self.has_max_value:
            initial_value = getattr(instance, self.initial_name)
            value = min(value, initial_value)
        setattr(instance, self.private_name, value)

    def get_rank_attribute_value(self, rank:int)-> int: 
        return self.rank_attributes[rank-2]

