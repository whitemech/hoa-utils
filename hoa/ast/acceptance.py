# -*- coding: utf-8 -*-
# This file is part of hoa-utils.
#
# hoa-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# hoa-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with hoa-utils.  If not, see <https://www.gnu.org/licenses/>.
#
"""This module contains the definitions of acceptance atoms."""
from dataclasses import dataclass
from enum import Enum
from functools import reduce, singledispatch
from typing import Optional, Set, Tuple, Union

from hoa.ast.boolean_expression import (
    BinaryOp,
    boolean_op_wrapper,
    FalseFormula,
    PositiveAnd,
    PositiveOr,
    TrueFormula,
    UnaryOp,
)
from hoa.types import ACCEPTANCE_PARAMETER, identifier


class AtomType(Enum):
    """This is an enumeration to represent the possible atom types."""

    FINITE = "Fin"
    INFINITE = "Inf"

    def __str__(self):
        """Get the string representation."""
        return self.value


@boolean_op_wrapper(
    and_=PositiveAnd["AcceptanceCondition"],
    or_=PositiveOr["AcceptanceCondition"],
    not_=None,
)
@dataclass(order=True, unsafe_hash=True, frozen=True)
class AcceptanceAtom:
    """Implement the acceptance atom."""

    atom_type: AtomType
    acceptance_set: int
    negated: bool

    def __invert__(self):
        """Negate the atom."""
        return AcceptanceAtom(self.atom_type, self.acceptance_set, not self.negated)


def Fin(acceptance_set: int):
    """Return the acceptance atom with finite acceptance."""
    return AcceptanceAtom(AtomType.FINITE, acceptance_set, False)


def NotFin(acceptance_set: int):
    """
    Return the acceptance atom with finite acceptance negated'.

    >>> not_fin0 = NotFin(0)
    >>> fin0 = Fin(0)
    >>> not_fin0 == ~fin0
    True
    """
    return ~Fin(acceptance_set)


def Inf(acceptance_set: int):
    """Return the acceptance atom with infinite acceptance."""
    return AcceptanceAtom(AtomType.INFINITE, acceptance_set, False)


def NotInf(acceptance_set: int):
    """
    Return the acceptance atom with infinite acceptance negated.

    >>> not_inf0 = NotInf(0)
    >>> inf0 = Inf(0)
    >>> not_inf0 == ~inf0
    True
    """
    return ~Inf(acceptance_set)


AcceptanceCondition = Union[
    PositiveAnd["AcceptanceCondition"],
    PositiveOr["AcceptanceCondition"],
    AcceptanceAtom,
    FalseFormula,
    TrueFormula,
]


@singledispatch
def accepting_sets(_) -> Set[int]:
    """
    Compute the accepting sets of an acceptance condition.

    :param _: the acceptance condition formula.
    :return: the set of accepting sets.
    """
    return set()


@accepting_sets.register  # type: ignore
def _(acceptance_condition: BinaryOp):
    return reduce(
        lambda x, y: x.union(y), map(accepting_sets, acceptance_condition.operands)
    )


@accepting_sets.register  # type: ignore
def _(acceptance_condition: UnaryOp):
    return accepting_sets(acceptance_condition.argument)


@accepting_sets.register  # type: ignore
def _(acceptance_condition: AcceptanceAtom):
    return {acceptance_condition.acceptance_set}


def nb_accepting_sets(acceptance_condition: AcceptanceCondition):
    """Get the number of accepting sets."""
    return len(accepting_sets(acceptance_condition))


@dataclass(order=True, unsafe_hash=True, frozen=True)
class Acceptance:
    """This class represents the acceptance in the HOA format."""

    condition: AcceptanceCondition
    name: Optional[identifier] = None
    parameters: Tuple[ACCEPTANCE_PARAMETER, ...] = tuple()
