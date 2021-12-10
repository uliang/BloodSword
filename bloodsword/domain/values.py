from __future__ import annotations

from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty
from dataclasses import dataclass, field
from math import floor
from typing import Optional

from .enumeration import Square


@dataclass
class Vector:
    """
    Representation of a 2d vector. 

    We follow the convention where the origin is located at the top left corner
    of the map. 
    """
    _x: int = 0
    _y: int = 0

    def __repr__(self):
        return repr((self.x, self.y))

    @abstractmethod
    def __add__(self, vec: Vector) -> Vector: 
        ... 

    @abstractmethod
    def __sub__(self, vec: Vector) -> Vector: 
        ... 

    @abstractproperty
    def coef_x(self) -> int: 
        """
        Decompose v = ae1 + be2 and return a. 
        """ 
    
    @abstractproperty
    def coef_y(self) -> int: 
        """
        Decompose v = ae1 + be2 and return b.
        """
    
    @abstractproperty
    def max_coef_xy(self) -> int: 
        """
        Returns the larger of the two coefficients of v. 
        """


@dataclass(frozen=True)
class Dice(ABC):
    """
    Subclass to provide logic for Dice object.
    """
    _n: int
    _n_faces: int = 6
    _modifier: Optional[int] = None

    @abstractclassmethod
    def from_string(cls, notation: str) -> Dice:
        """
        :param str notation: Die notation in XdY+Z. 
        :returns: Instance of Dice. 
        :rtype: Dice

        Factory function to create dice object from die notation. 
        """

    @abstractmethod
    def roll(self) -> Score:
        """
        Roll dice and obtain result as a Score object. 
        """


@dataclass(frozen=True, eq=True, order=True)
class Rank(ABC):
    """
    Value object for representing the power level of character, current XP and
    whether character should advance in rank.
    """
    _rank: int = field(compare=True)
    _xp: int = field(compare=False)
    _breakpoint: int = field(compare=False)

    @property
    def rank(self) -> int:
        """
        :returns: Power level of character.
        :rtype: int
        """
        return self._rank

    def __repr__(self) -> str:
        return repr(self._rank)

    @abstractmethod
    def should_advance(self, with_xp: int) -> bool:
        """
        :param int with_xp: Amount of additional xp awarded.
        :returns: True if new rank is attained, False otherwise.
        :rtype: bool

        Implement logic to test whether a new rank is attained. ::

            >>> r = Rank(2, 250, 499)
            >>> r.should_advance(300)
            True
            >>> r.should_advance(200)
            False
        """


@dataclass(frozen=True, eq=True, order=True)
class Score(ABC):
    """
    Subclass this abstract class to implement rules for attribute values.
    E.g., the fact that endurance cannot exceed it's initial value. 

    Score attempts to emulate numeric types. ::

        >>> x = Score(7,7)
        >>> x + Score(5)
        12
        >>> x - Score(1)
        6
        >>> x*2
        14
        >>> x/3
        2
    """
    _value: int = field(compare=True)
    _initial_value: Optional[int] = field(compare=False, default=None)

    def __repr__(self) -> str:
        return repr(self._value)

    def __add__(self, value: Score):
        a = self._increment(value)
        return Score(a, self._initial_value)

    def __sub__(self, value: Score):
        return Score(max(0, self._value - value._value), self._initial_value)

    def __mul__(self, value: int):
        return Score(self._data*value, self._initial_value)

    def __div__(self, value: int):
        """
        Results are always rounded down. 
        """
        return Score(floor(self._value/value), self._initial_value)

    @abstractmethod
    def _increment(self, value: Score) -> int:
        """
        Override this method to implement special rules for incrementing the
        attribute. 
        """
