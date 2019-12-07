# -*- coding: utf-8 -*-
"""This module contains the definition of the HOA parser."""

import logging
import os
from pathlib import Path
from typing import Any, Dict

from lark import Lark, Transformer

from hoa2dot.core import TrueAcceptance, FalseAcceptance, And, Or, Not, AtomType, Atom, Acceptance, HOAHeader, \
    AliasLabelExpression

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
        args[0].dumps()
        return args[0]

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
            if header_item_type in {HeaderItemType.ALIAS, HeaderItemType.START_STATES, HeaderItemType.PROPERTIES}:
                headertype2value.setdefault(header_item_type, []).extend(value if isinstance(value, list) else [value])
            else:
                assert header_item_type not in headertype2value
                headertype2value[header_item_type] = value

        assert HeaderItemType.ACCEPTANCE in headertype2value, "'Acceptance:' must always be present."

        return HOAHeader(
            format_version,
            acceptance=headertype2value[HeaderItemType.ACCEPTANCE],
            nb_states=headertype2value.get(HeaderItemType.NUM_STATES, None),
            start_states=headertype2value.get(HeaderItemType.START_STATES, None),
            acceptance_name=headertype2value.get(HeaderItemType.ACCEPTANCE_NAME, None),
            propositions=headertype2value.get(HeaderItemType.PROPOSITIONS, None),
            tool=headertype2value.get(HeaderItemType.TOOL, None),
            name=headertype2value.get(HeaderItemType.NAME, None),
            properties=headertype2value.get(HeaderItemType.PROPERTIES, None))

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
        return HeaderItemType.NAME, args[0]

    def properties(self, args):
        """Parse the 'automaton' node."""
        return HeaderItemType.PROPERTIES, args

    def headername(self, args):
        """Parse the 'automaton' node."""
        key, values = args[0], args[1:]
        return HeaderItemType.HEADERNAME, (key, values)

    def body(self, args):
        """Parse the 'automaton' node."""
        pass

    def state_name(self, args):
        """Parse the 'automaton' node."""
        pass

    def acc_sig(self, args):
        """Parse the 'automaton' node."""
        pass

    def edge(self, args):
        """Parse the 'automaton' node."""
        pass

    def label(self, args):
        """Parse the 'automaton' node."""
        pass

    def state_conj(self, args):
        """Parse the 'automaton' node."""
        return args

    def label_expr(self, args):
        """Parse the 'automaton' node."""
        pass

    def or_label_expr(self, args):
        """Parse the 'or_label_expr' node."""
        pass

    def and_label_expr(self, args):
        """Parse the 'and_label_expr' node."""
        pass

    def not_label_expr(self, args):
        """Parse the 'not_label_expr' node."""
        pass

    def alias_label_expr(self, args):
        """Parse the 'alias_label_expr' node."""
        pass

    def atom_label_expr(self, args):
        """Parse the 'atom_label_expr' node."""
        pass

    def boolean_label_expr(self, args):
        """Parse the 'boolean_label_expr' node."""
        pass

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
        return And(args)

    def or_acceptance_cond(self, args):
        """Parse the 'or_acceptance_cond' node."""
        return Or(args)

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
