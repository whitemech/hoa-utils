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
from dataclasses import dataclass
from typing import Any, ClassVar, Collection, Generic, Optional, Sequence, Type, TypeVar

T = TypeVar("T")


@dataclass(order=True, unsafe_hash=True, frozen=True)
class BinaryOp(Generic[T]):
    """Binary operator."""

    SYMBOL: ClassVar[str]
    operands: Sequence[T]

    def __str__(self) -> str:
        """Get the string representation."""
        return f"({self.SYMBOL} {' '.join(map(str, self.operands))})"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"{type(self).__name__}({repr(self.operands)})"


@dataclass(order=True, unsafe_hash=True, frozen=True)
class UnaryOp(Generic[T]):
    """Unary operator."""

    SYMBOL: ClassVar[str]
    argument: T

    def __str__(self) -> str:
        """Get the string representation."""
        return f"({self.SYMBOL} {self.argument})"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"{type(self).__name__}({repr(self.argument)})"


@dataclass(order=True, unsafe_hash=True, frozen=True)
class TrueFormula:
    """A tautology."""

    def __str__(self) -> str:
        """Get the string representation."""
        return "(true)"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return "TrueFormula()"

    def __neg__(self) -> "FalseFormula":
        """Negate."""
        return FALSE


@dataclass(order=True, unsafe_hash=True, frozen=True)
class FalseFormula:
    """A contradiction."""

    def __str__(self) -> str:
        """Get the string representation."""
        return "(false)"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return "FalseFormula()"

    def __neg__(self) -> "TrueFormula":
        """Negate."""
        return TRUE


TRUE = TrueFormula()
FALSE = FalseFormula()


class MonotoneOp(type):
    """Metaclass to simplify monotone operator instantiations."""

    _absorbing: ClassVar[Optional[Any]] = None

    def __call__(cls, *args, **kwargs):
        """Init the subclass object."""
        operands = _simplify_monotone_op_operands(cls, *args)
        if len(operands) == 1:
            return operands[0]

        return super(MonotoneOp, cls).__call__(operands, **kwargs)


class _And(BinaryOp, Generic[T], metaclass=MonotoneOp):
    """And operator."""

    _absorbing = FALSE
    SYMBOL = "&"


class _Or(BinaryOp, Generic[T], metaclass=MonotoneOp):
    """Or operator."""

    _absorbing = TRUE
    SYMBOL = "|"


class _PositiveAnd(BinaryOp, Generic[T], metaclass=MonotoneOp):
    """And operator."""

    _absorbing = FALSE
    SYMBOL = "&"


class _PositiveOr(BinaryOp, Generic[T], metaclass=MonotoneOp):
    """Or operator."""

    _absorbing = TRUE
    SYMBOL = "|"


class _Not(UnaryOp, Generic[T]):
    """Not operator."""

    SYMBOL = "!"


# _cls should never be specified by keyword, so start it with an
# underscore.  The presence of _cls is used to detect if this
# decorator is being called with parameters or not.
def boolean_op_wrapper(
    _cls=None,
    *,
    and_: Optional[Type[BinaryOp]] = _And,
    or_: Optional[Type[BinaryOp]] = _Or,
    not_: Optional[Type[BinaryOp]] = _Not,
):
    """
    Provide the atom class with __and__, __or__ and __not__ dunder methods.

    :param _cls: the class.
    :param and_: the class for the __and__ operation
    :param or_: the class for the __or__ operation
    :param not_: the class for the __not__ operation
    :return: the same class, endowed with new dunder methods.
    """

    def _process_class(cls, and_cls, or_cls, not_cls):
        if and_cls is not None:
            cls.__and__ = lambda self, other: and_cls(self, other)
        if or_cls is not None:
            cls.__or__ = lambda self, other: or_cls(self, other)
        if not_cls is not None:
            cls.__invert__ = lambda self: not_cls(self)
        return cls

    def wrap(cls):
        return _process_class(cls, and_, or_, not_)

    if _cls is None:
        return wrap

    return wrap(_cls)


And = boolean_op_wrapper(_cls=_And)
Or = boolean_op_wrapper(_cls=_Or)
Not = boolean_op_wrapper(_cls=_Not)

PositiveAnd = boolean_op_wrapper(_cls=_PositiveAnd, and_=_PositiveAnd, or_=_PositiveOr)
PositiveOr = boolean_op_wrapper(_cls=_PositiveOr, and_=_PositiveAnd, or_=_PositiveOr)


def ensure_formula(f: Optional[T], is_none_true: bool) -> T:
    """
    Ensure the argument is a formula.

    :param f: the formula, or None.
    :param is_none_true: if true, None reduces to TrueFormula; FalseFormula otherwise.
    :return: the same set, or an empty set if the arg was None.
    """
    return f if f is not None else TrueFormula() if is_none_true else FalseFormula()


def _simplify_monotone_op_operands(cls, *operands):
    operands = list(dict.fromkeys(operands))
    if len(operands) == 0:
        return (~cls._absorbing,)
    elif len(operands) == 1:
        return (operands[0],)
    elif cls._absorbing in operands:
        return cls._absorbing

    # shift-up subformulas with same operator. DFS on expression tree.
    new_operands = []
    stack = operands[::-1]  # it is reversed in order to preserve order.
    while len(stack) > 0:
        element = stack.pop()
        if not isinstance(element, cls):
            new_operands.append(element)
            continue
        stack.extend(reversed(element.operands))  # see above regarding reversed.

    return tuple(new_operands)
