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

"""This module contains the core definitions for the tool."""
from dataclasses import dataclass
from typing import AbstractSet, Dict, FrozenSet, Optional, Sequence, Tuple, Union

from hoa.ast.acceptance import Acceptance
from hoa.ast.label import LabelAlias, LabelExpression
from hoa.types import HEADER_VALUES, headername, identifier, string


@dataclass(frozen=True, order=True, unsafe_hash=True)
class State:
    """This class represents a state of the automaton."""

    index: int
    label: Optional[LabelExpression] = None
    name: Optional[string] = None
    acc_sig: Optional[FrozenSet[int]] = None


@dataclass(frozen=True, order=True)
class Edge:
    """This class represents an edge in the automaton."""

    state_conj: Sequence[int]
    label: Optional[LabelExpression] = None
    acc_sig: Optional[AbstractSet[int]] = None


@dataclass(frozen=True)
class HOAHeader:
    """This class implements a data structure for the HOA file format header."""

    format_version: identifier
    acceptance: Acceptance
    nb_states: Optional[int] = None
    start_states: Optional[AbstractSet[AbstractSet[int]]] = None
    propositions: Optional[Tuple[string, ...]] = None
    aliases: Optional[Sequence[LabelAlias]] = None
    tool: Optional[Union[string, Sequence[string]]] = None
    name: Optional[string] = None
    properties: Optional[Sequence[identifier]] = None
    headernames: Optional[Dict[headername, Sequence[HEADER_VALUES]]] = None


@dataclass(frozen=True)
class HOABody:
    """This class implements a data structure for the HOA file format header."""

    state2edges: Dict[State, Sequence[Edge]]


@dataclass(frozen=True)
class HOA:
    """This class implements a data structure for the HOA file format."""

    header: HOAHeader
    body: HOABody
