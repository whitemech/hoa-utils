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
from pathlib import Path
from typing import AbstractSet, Any, Callable, Collection, Optional, Sequence


def _get_current_path() -> Path:
    """Get the path to the file where the function is called."""
    import inspect
    import os

    return Path(os.path.dirname(inspect.getfile(inspect.currentframe())))  # type: ignore


def _assert(condition: bool, message: str = ""):
    """User-defined assert."""
    if not condition:
        raise AssertionError(message)


def ensure(arg: Optional[Any], default: Any):
    """Ensure an object is not None, or return a default."""
    return arg if arg is not None else default


def ensure_set(arg: Optional[Collection], immutable: bool = True) -> AbstractSet:
    """
    Ensure the argument is a set.

    :param arg: the set, or None.
    :param immutable: whether the collection should be immutable.
    :return: the same set, or an empty set if the arg was None.
    """
    op = frozenset if immutable else set
    return op(arg) if arg is not None else op()


def ensure_sequence(arg: Optional[Sequence], immutable: bool = True) -> Sequence:
    """
    Ensure the argument is a sequence.

    :param arg: the list, or None.
    :param immutable: whether the collection should be immutable.
    :return: the same list, or an empty list if the arg was None.
    """
    op: Callable = tuple if immutable else list
    return op(arg) if arg is not None else op()


def safe_index(seq: Sequence, *args, **kwargs):
    """Find element, safe."""
    try:
        return seq.index(*args, **kwargs)
    except ValueError:
        return None


def safe_get(seq: Sequence, index: int, default=None):
    """Get element at index, safe."""
    return seq[index] if index < len(seq) else default
