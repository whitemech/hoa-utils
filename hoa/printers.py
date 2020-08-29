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

"""This module contains functions to print acceptance conditions and label expressions."""

from functools import singledispatch

from hoa.ast.acceptance import AcceptanceAtom, AcceptanceCondition
from hoa.ast.boolean_expression import BinaryOp, FalseFormula, TrueFormula, UnaryOp
from hoa.ast.label import LabelAlias, LabelAtom, LabelExpression


@singledispatch
def acceptance_condition_to_string(_: AcceptanceCondition):
    """Transform an acceptance condition into a string."""
    return str(_)


@acceptance_condition_to_string.register  # type: ignore
def _(f: AcceptanceAtom):
    """Transform an acceptance atom into a string."""
    return f"{f.atom_type.value}({'!' if f.negated else ''}{f.acceptance_set})"


@acceptance_condition_to_string.register  # type: ignore
def _(f: BinaryOp):
    """Transform a binary operation over acceptance formulas into a string."""
    return (
        "("
        + f" {f.SYMBOL} ".join(map(acceptance_condition_to_string, f.operands))
        + ")"
    )


@acceptance_condition_to_string.register  # type: ignore
def _(_acceptance_condition: TrueFormula):
    """Transform true into a string."""
    return "t"


@acceptance_condition_to_string.register  # type: ignore
def _(_acceptance_condition: FalseFormula):
    """Transform false into a string."""
    return "f"


@singledispatch
def label_expression_to_string(_: LabelExpression):
    """Transform a label expression into a string."""
    return str(_)


@label_expression_to_string.register  # type: ignore
def _(f: LabelAtom):
    """Transform a label atom into a string."""
    return f"{f.proposition}"


@label_expression_to_string.register  # type: ignore
def _(f: LabelAlias):
    """Transform a label alias into a string."""
    return f"{f.alias}"


@label_expression_to_string.register  # type: ignore
def _(f: BinaryOp):
    """Transform a binary operation over labels into a string."""
    return "(" + f" {f.SYMBOL} ".join(map(label_expression_to_string, f.operands)) + ")"


@label_expression_to_string.register  # type: ignore
def _(f: UnaryOp):
    """Transform a unary operation over labels into a string."""
    return f"({f.SYMBOL}{label_expression_to_string(f.argument)})"


@label_expression_to_string.register  # type: ignore
def _(_f: TrueFormula):
    """Transform a true formula into a string."""
    return "t"


@label_expression_to_string.register  # type: ignore
def _(_f: FalseFormula):
    """Transform a false formula into a string."""
    return "f"
