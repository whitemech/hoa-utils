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
from functools import reduce, singledispatch
from typing import Optional, Set, Union

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


@propositions.register
def _(label_expression: BinaryOp):
    return reduce(lambda x, y: x.union(y), map(propositions, label_expression.operands))


@propositions.register
def _(label_expression: UnaryOp):
    return propositions(label_expression.argument)


@propositions.register
def _(label_expression: LabelAtom):
    return {label_expression.proposition}


@propositions.register
def _(label_expression: LabelAlias):
    return propositions(label_expression.expression)
