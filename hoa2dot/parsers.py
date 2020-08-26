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

"""This module contains the definition of the HOA parser."""

import logging
import operator
import os
from collections import OrderedDict
from functools import reduce
from pathlib import Path
from typing import Any, Dict, List

from lark import Lark, Transformer, Tree

from hoa2dot.core import (
    HOA,
    Acceptance,
    AliasLabelExpression,
    And,
    AndLabelExpression,
    Atom,
    AtomLabelExpression,
    AtomType,
    Edge,
    FalseAcceptance,
    FalseLabelExpression,
    HOABody,
    HOAHeader,
    Not,
    NotLabelExpression,
    Or,
    OrLabelExpression,
    State,
    TrueAcceptance,
    TrueLabelExpression,
)

logger = logging.getLogger(__name__)


class HeaderItemType:
    """Enumeration of header types."""

    NUM_STATES = "num_states"
    START_STATES = "start_state"
    PROPOSITIONS = "propositions"
    ALIAS = "alias"
    ACCEPTANCE = "acceptance"
    ACCEPTANCE_NAME = "acc_name"
    TOOL = "tool"
    NAME = "name"
    PROPERTIES = "properties"
    HEADERNAME = "headername"


class HOATransformer(Transformer):
    """The transformer of the AST of the tool to a more handy data structure."""

    def __init__(self):
        """Initialize the transformer."""
        super().__init__(visit_tokens=True)

    INT = int
    STRING = str
    IDENTIFIER = str
    HEADERNAME = str

    def BOOLEAN(self, args):
        """Define BOOLEAN types."""
        label = args[0]
        if label == "t":
            return True
        elif label == "f":
            return False
        else:
            raise ValueError("Should not be here.")

    def start(self, args):
        """Parse the 'start' node."""
        return args[0]

    def automaton(self, args):
        """Parse the 'automaton' node."""
        return HOA(args[0], args[1])

    def header(self, args):
        """Parse the 'header' node.

        The header is a list of header-items (a HEADERNAME followed by some data).
        Except for the "HOA:" item, which should always come first,
        the items may occur in any order. Some HEADERNAMEs have predefined
        semantics (and might be mandatory) as specified below. This format also
        makes provision of additional (unspecified) header names to be used.

        Any given HEADERNAME should occur at most once, except for Start:, Alias:, and properties:.
        The case of the HEADERNAME's initial is used to specify whether tools may
        safely ignore a header item they do not support: header items whose name
        start with an upper-case letter are expected to influence the semantic of
        the automaton: tools should at least warn about any such HEADERNAME they do not understand.
        A HEADERNAME whose initial is lowercase may be safely ignored without affecting the semantics.

        Headers items HOA:, and Acceptance: must always be present.
        """
        format_version = args[0]
        assert isinstance(format_version, str), "The first item should be the version."

        headertype2value = {}  # type: Dict[HeaderItemType, Any]
        for header_item_type, value in args[1:]:
            if header_item_type in {
                HeaderItemType.ALIAS,
                HeaderItemType.START_STATES,
                HeaderItemType.PROPERTIES,
            }:
                headertype2value.setdefault(header_item_type, []).extend(
                    value if isinstance(value, list) else [value]
                )
            else:
                assert header_item_type not in headertype2value
                headertype2value[header_item_type] = value

        assert (
            HeaderItemType.ACCEPTANCE in headertype2value
        ), "'Acceptance:' must always be present."

        return HOAHeader(
            format_version,
            acceptance=headertype2value[HeaderItemType.ACCEPTANCE],
            nb_states=headertype2value.get(HeaderItemType.NUM_STATES, None),
            start_states=headertype2value.get(HeaderItemType.START_STATES, None),
            aliases=headertype2value.get(HeaderItemType.ALIAS, None),
            acceptance_name=headertype2value.get(HeaderItemType.ACCEPTANCE_NAME, None),
            propositions=headertype2value.get(HeaderItemType.PROPOSITIONS, None),
            tool=headertype2value.get(HeaderItemType.TOOL, None),
            name=headertype2value.get(HeaderItemType.NAME, None),
            properties=headertype2value.get(HeaderItemType.PROPERTIES, None),
        )

    def format_version(self, args):
        """Parse the 'format_version' node."""
        return args[0]

    def header_item(self, args):
        """Parse the 'header_item' node."""
        return args[0]

    def num_states(self, args):
        """Parse the 'num_states' node."""
        return HeaderItemType.NUM_STATES, args[0]

    def start_state(self, args):
        """Parse the 'start_state' node."""
        return HeaderItemType.START_STATES, args[0]

    def propositions(self, args):
        """Parse the 'propositions' node."""
        return HeaderItemType.PROPOSITIONS, tuple(prop[1:-1] for prop in args[1:])

    def alias(self, args):
        """Parse the 'alias' node."""
        alias_name = args[0]
        label_expression = args[1]
        return HeaderItemType.ALIAS, AliasLabelExpression(alias_name, label_expression)

    def acceptance(self, args):
        """Parse the 'acceptance' node."""
        nb_accepting_sets = args[0]
        acceptance_condition = args[1]
        accepting_sets = acceptance_condition.accepting_sets
        # this checks whether the number of acc. sets in the acceptance condition is correct.
        assert max(accepting_sets) == len(accepting_sets) - 1 == nb_accepting_sets - 1
        return HeaderItemType.ACCEPTANCE, Acceptance(acceptance_condition)

    def acc_name(self, args):
        """Parse the 'acc_name' node."""
        return HeaderItemType.ACCEPTANCE_NAME, " ".join(map(str, args))

    def tool(self, args):
        """Parse the 'tool' node."""
        return HeaderItemType.TOOL, args[0]

    def name(self, args):
        """Parse the 'nome' node."""
        return HeaderItemType.NAME, args[0].strip('"')

    def properties(self, args):
        """Parse the 'automaton' node."""
        return HeaderItemType.PROPERTIES, args

    def headername(self, args):
        """Parse the 'automaton' node."""
        key, values = args[0], args[1:]
        return HeaderItemType.HEADERNAME, (key, values)

    def body(self, args):
        """Parse the 'body' node."""
        state2edges = OrderedDict({})  # type: Dict[State, List[Edge]]
        current_state = None
        for arg in args:
            if isinstance(arg, State):
                current_state = arg
                state2edges[current_state] = []
            elif isinstance(arg, Edge):
                state2edges[current_state].append(arg)
        return HOABody(state2edges)

    def state_name(self, args):
        """Parse the 'state_name' node."""
        non_trees = [arg for arg in args if not isinstance(arg, Tree)]
        kwargs = {arg.data: arg.children[0] for arg in args if isinstance(arg, Tree)}

        if "acc_sig" in kwargs.keys():
            kwargs["acc_sig"] = frozenset({kwargs["acc_sig"]})

        if len(non_trees) == 1:
            return State(index=non_trees[0], **kwargs)
        elif len(non_trees) == 2:
            return State(index=non_trees[0], name=non_trees[1].strip('"'), **kwargs)
        else:
            raise ValueError("Should not be here.")

    def edge(self, args):
        """Parse the 'edge' node."""
        if len(args) == 1:
            return Edge(args[0])
        elif len(args) == 2:
            # either 'label state_conj' or 'state_conj acc-sig'
            first, second = args
            if isinstance(first, Tree):
                return Edge(second, label=first.children[0])
            else:
                return Edge(
                    first, acc_sig=frozenset(second.children)
                )  # acc_sig as frozenset()
        elif len(args) == 3:
            label, state_conj, acc_sig = (
                args[0].children[0],
                args[1],
                frozenset(args[2].children),
            )
            return Edge(state_conj, label=label, acc_sig=acc_sig)
        else:
            raise ValueError("Should not be here.")

    def state_conj(self, args):
        """Parse the 'state_conj' node."""
        # compute the flat list
        return list(
            reduce(
                operator.add, map(lambda x: [x] if not isinstance(x, list) else x, args)
            )
        )

    def label_expr(self, args):
        """Parse the 'label_expr' node."""
        return args[0]

    def or_label_expr(self, args):
        """Parse the 'or_label_expr' node."""
        return OrLabelExpression(args)

    def and_label_expr(self, args):
        """Parse the 'and_label_expr' node."""
        return AndLabelExpression(args)

    def not_label_expr(self, args):
        """Parse the 'not_label_expr' node."""
        return NotLabelExpression(args[0])

    def alias_label_expr(self, args):
        """Parse the 'alias_label_expr' node."""
        return AliasLabelExpression(alias=args[0], expression=None)

    def atom_label_expr(self, args):
        """Parse the 'atom_label_expr' node."""
        return AtomLabelExpression(str(args[0]))

    def boolean_label_expr(self, args):
        """Parse the 'boolean_label_expr' node."""
        boolean = args[0]
        if boolean is True:
            return TrueLabelExpression()
        elif boolean is False:
            return FalseLabelExpression()
        else:
            raise ValueError("Should not be here.")

    def acceptance_cond(self, args):
        """Parse the 'acceptance_cond' node."""
        return args[0]

    def atom_acceptance_cond(self, args):
        """Parse the 'atom_acceptance_cond' node."""
        atom_type = AtomType(args[0])
        accepting_set = args[1]
        return Atom(accepting_set, atom_type)

    def not_acceptance_cond(self, args):
        """Parse the 'not_acceptance_cond' node."""
        atom_type = AtomType(args[0])
        accepting_set = args[1]
        return Not(accepting_set, atom_type)

    def and_acceptance_cond(self, args):
        """Parse the 'and_acceptance_cond' node."""
        return And(
            list(
                reduce(
                    lambda x, y: x + y,
                    map(lambda x: x.conditions if isinstance(x, And) else [x], args),
                )
            )
        )

    def or_acceptance_cond(self, args):
        """Parse the 'or_acceptance_cond' node."""
        return Or(
            list(
                reduce(
                    lambda x, y: x + y,
                    map(lambda x: x.conditions if isinstance(x, Or) else [x], args),
                )
            )
        )

    def boolean_acceptance_cond(self, args):
        """Parse the 'boolean_acceptance_cond' node."""
        boolean = args[0]
        assert type(boolean) == bool
        if boolean:
            return TrueAcceptance()
        else:
            return FalseAcceptance()


class HOAParser:
    """The parser for the HOA format."""

    def __init__(self):
        """Initialize the HOA parser."""
        directory = Path(os.path.dirname(os.path.realpath(__file__)))
        self._transformer = HOATransformer()
        self._parser = Lark(open(directory / "grammars" / "hoa.lark"))

    def __call__(self, text: str):
        """Try to parse a string."""
        tree = self._parser.parse(text)
        result = self._transformer.transform(tree)
        return result
