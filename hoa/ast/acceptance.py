# -*- coding: utf-8 -*-
#
# MIT License
#
# Copyright (c) 2020 Whitemech
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""This module contains the definitions of acceptance atoms."""
from dataclasses import dataclass
from enum import Enum
from functools import reduce, singledispatch
from typing import Optional, Sequence, Set, Tuple, Union

from hoa.ast.boolean_expression import (
    And,
    BinaryOp,
    boolean_op_wrapper,
    FalseFormula,
    Not,
    Or,
    PositiveAnd,
    PositiveOr,
    TrueFormula,
    UnaryOp,
)
from hoa.types import acceptance_parameter, ACCEPTANCE_PARAMETER, identifier


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
    return AcceptanceAtom(AtomType.FINITE, acceptance_set, False)


def NotFin(acceptance_set: int):
    return ~Fin(acceptance_set)


def Inf(acceptance_set: int):
    return AcceptanceAtom(AtomType.INFINITE, acceptance_set, False)


def NotInf(acceptance_set: int):
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


@accepting_sets.register
def _(acceptance_condition: BinaryOp):
    return reduce(
        lambda x, y: x.union(y), map(accepting_sets, acceptance_condition.operands)
    )


@accepting_sets.register
def _(acceptance_condition: UnaryOp):
    return accepting_sets(acceptance_condition.argument)


@accepting_sets.register
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
