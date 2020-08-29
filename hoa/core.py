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
