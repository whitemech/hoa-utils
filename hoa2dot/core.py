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
from typing import (
    AbstractSet,
    Dict,
    FrozenSet,
    Optional,
    Sequence,
    TextIO,
    Tuple,
    Union,
)

from hoa2dot.ast.acceptance import Acceptance
from hoa2dot.ast.label import LabelAlias, LabelExpression
from hoa2dot.types import HEADER_VALUES, headername, identifier, string


@dataclass(frozen=True, order=True, unsafe_hash=True)
class State:
    """This class represents a state of the automaton."""

    index: int
    label: Optional[LabelExpression] = None
    name: Optional[string] = None
    acc_sig: Optional[FrozenSet[int]] = None

    def to_hoa_repr(self) -> str:
        """Get the HOA format representation of the state."""
        s = "State: "
        if self.label is not None:
            s += "[" + str(self.label) + "]" + " "
        s += str(self.index) + " "
        if self.name is not None:
            s += '"' + self.name + '"' + " "
        if self.acc_sig is not None:
            s += "{" + " ".join(map(str, self.acc_sig)) + "}"
        return s


@dataclass(frozen=True, order=True)
class Edge:
    """This class represents an edge in the automaton."""

    state_conj: Sequence[int]
    label: Optional[LabelExpression] = None
    acc_sig: Optional[AbstractSet[int]] = None

    def to_hoa_repr(self) -> str:
        """Get the HOA format representation of the edge."""
        s = ""
        if self.label is not None:
            s += "[" + str(self.label) + "]" + " "
        s += "&".join(map(str, self.state_conj)) + " "
        if self.acc_sig is not None:
            s += "{" + " ".join(map(str, self.acc_sig)) + "}"
        return s


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

    def dumps(self) -> str:
        """
        Dump the header data into a string in HOA format.

        :return: the header string in HOA format.
        """
        s = "HOA: {}\n".format(self.format_version)
        if self.nb_states is not None:
            s += "States: {}\n".format(self.nb_states)
        if self.start_states is not None:
            s += "\n".join("Start: {}".format(idx) for idx in self.start_states) + "\n"
        if self.propositions is not None and len(self.propositions) > 0:
            propositions_string = '"' + '" "'.join(p for p in self.propositions) + '"'
            s += "AP: {nb} {prop}\n".format(
                nb=len(self.propositions), prop=propositions_string
            )
        if self.aliases is not None and len(self.aliases) > 0:
            s += (
                "\n".join(
                    [
                        "Alias: {} {}".format(
                            alias_label.alias, str(alias_label.expression)
                        )
                        for alias_label in self.aliases
                    ]
                )
                + "\n"
            )
        if self.acceptance_name is not None:
            s += "acc-name: {}\n".format(self.acceptance_name)
        s += self.acceptance.get_hoa_repr() + "\n"
        if self.tool is not None:
            s += "tool: {}\n".format(" ".join(self.tool))
        if self.name is not None:
            s += 'name: "{}"\n'.format(self.name)
        if self.properties is not None and len(self.properties) > 0:
            s += "properties: {}\n".format(" ".join(self.properties))
        if self.headernames is not None and len(self.headernames) > 0:
            s += (
                "\n".join(
                    [
                        "{}: {}".format(key, " ".join(values))
                        for key, values in self.headernames.items()
                    ]
                )
                + "\n"
            )

        return s


@dataclass(frozen=True)
class HOABody:
    """This class implements a data structure for the HOA file format header."""

    state2edges: Dict[State, Sequence[Edge]]

    def dumps(self) -> str:
        """
        Dump the body data into a string in HOA format.

        :return: the body string in HOA format.
        """
        return (
            "\n".join(
                [
                    state.to_hoa_repr()
                    + "\n"
                    + "\n".join(map(lambda x: x.to_hoa_repr(), edges))
                    for state, edges in self.state2edges.items()
                ]
            )
            + "\n"
        )


@dataclass(frozen=True)
class HOA:
    """This class implements a data structure for the HOA file format."""

    header: HOAHeader
    body: HOABody

    def dump(self, fp: TextIO) -> None:
        """
        Dump the data to a file.

        :param fp: the file pointer.
        :return: None.
        """
        fp.write(self.dumps())

    def dumps(self) -> str:
        """
        Dump the data into a string in HOA format.

        :return: the string in HOA format.
        """
        header = self.header.dumps()
        body = self.body.dumps()
        return header + "--BODY--\n" + body + "--END--"
