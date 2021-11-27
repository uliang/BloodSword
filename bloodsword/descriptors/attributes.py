from dataclasses import dataclass
from enum import Enum, auto


class AttrState(Enum):
    UNBOUNDED = auto()
    BOUNDED = auto()


@dataclass
class Attribute:
    has_max_value: bool = False
    min_value: int = 0

    def __set_name__(self, instance, name):
        self.private_name = '_' + name
        self.initial_name = f'_initial_{name}_value'
        self.attribute_state = f'_{name}_state'
        setattr(instance, self.attribute_state, AttrState.UNBOUNDED)

    def __get__(self, instance, type_=None):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        value = max(self.min_value, value)
        attribute_state = getattr(instance, self.attribute_state)
        if attribute_state is AttrState.UNBOUNDED:
            setattr(instance, self.private_name, value)
            if self.has_max_value:
                setattr(instance, self.initial_name, value)
                setattr(instance, self.attribute_state,  AttrState.BOUNDED)
        elif attribute_state is AttrState.BOUNDED:
            initial_value = getattr(instance, self.initial_name)
            setattr(instance, self.private_name, min(initial_value, value))
