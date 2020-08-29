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
from functools import reduce, singledispatch
from typing import Set, Union

from hoa.ast.boolean_expression import (
    And,
    BinaryOp,
    boolean_op_wrapper,
    FalseFormula,
    Not,
    Or,
    TrueFormula,
    UnaryOp,
)
from hoa.types import alias as alias_type


@boolean_op_wrapper(
    and_=And["LabelExpression"], or_=Or["LabelExpression"], not_=Not["LabelExpression"]
)
@dataclass(order=True, unsafe_hash=True, frozen=True)
class LabelAtom:
    """Implement the label atom."""

    proposition: int


@boolean_op_wrapper(
    and_=And["LabelExpression"], or_=Or["LabelExpression"], not_=Not["LabelExpression"]
)
@dataclass(order=True, unsafe_hash=True, frozen=True)
class LabelAlias:
    """Implement the label alias."""

    alias: alias_type
    expression: "LabelExpression"


LabelExpression = Union[
    And["LabelExpression"],
    Or["LabelExpression"],
    Not["LabelExpression"],
    LabelAtom,
    LabelAlias,
    FalseFormula,
    TrueFormula,
]


@singledispatch
def propositions(_) -> Set[int]:
    """
    Compute the accepting sets of an acceptance condition.

    :param _: the acceptance condition formula.
    :return: the set of accepting sets.
    """
    return set()


@propositions.register  # type: ignore
def _(label_expression: BinaryOp):
    return reduce(lambda x, y: x.union(y), map(propositions, label_expression.operands))


@propositions.register  # type: ignore
def _(label_expression: UnaryOp):
    return propositions(label_expression.argument)


@propositions.register  # type: ignore
def _(label_expression: LabelAtom):
    return {label_expression.proposition}


@propositions.register  # type: ignore
def _(label_expression: LabelAlias):
    return propositions(label_expression.expression)
