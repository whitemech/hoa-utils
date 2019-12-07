# -*- coding: utf-8 -*-
"""This module contains the core definitions for the tool."""
from abc import ABC, abstractmethod
from enum import Enum
from functools import reduce
from os import PathLike
from typing import Optional, List, Set, Dict, Tuple


class AcceptanceCondition(ABC):
    """This class implements the acceptance condition."""

    @abstractmethod
    def __str__(self):
        """Transform the object to string."""

    @property
    @abstractmethod
    def accepting_sets(self) -> Set[int]:
        """Get the set of accepting sets."""

    @property
    def nb_accepting_sets(self) -> int:
        """Get the number of accepting sets."""
        return len(self.accepting_sets)


class AtomType(Enum):
    """This is an enumeration to represent the possible atom types."""
    FINITE = "Fin"
    INFINITE = "Inf"


class And(AcceptanceCondition):
    """This class implements a conjunction between acceptance conditions."""

    def __init__(self, conditions: List[AcceptanceCondition]):
        """
        Initialize the conjunction.

        :param conditions: the operands of the condition.
        """
        self._conditions = conditions

    @property
    def conditions(self) -> List[AcceptanceCondition]:
        """Get the subformulas."""
        return self._conditions

    @property
    def accepting_sets(self) -> Set[int]:
        """Get the set of accepting sets."""
        return reduce(lambda x, y: x.union(y), map(lambda x: x.accepting_sets, self.conditions))

    def __str__(self):
        return " ".join(map(str, self.conditions))


class Or(AcceptanceCondition):
    """This class implements a disjunction between acceptance conditions."""

    def __init__(self, conditions: List[AcceptanceCondition]):
        """
        Initialize the disjunction.

        :param conditions: the operands of the condition.
        """
        self._conditions = conditions

    @property
    def conditions(self) -> List[AcceptanceCondition]:
        """Get the subformulas."""
        return self._conditions

    @property
    def accepting_sets(self) -> Set[int]:
        """Get the set of accepting sets."""
        return reduce(lambda x, y: x.union(y), map(lambda x: x.accepting_sets, self.conditions))

    def __str__(self):
        return " ".join(map(str, self.conditions))


class Atom(AcceptanceCondition):
    """This class is an atom in the acceptance condition."""

    def __init__(self, accepting_set: int, atom_type: AtomType):
        """
        Initialize an atom.

        :param accepting_set: the accepting set.
        :param atom_type: the type of the atom.
        """
        self._accepting_set = accepting_set
        self._atom_type = atom_type

    @property
    def accepting_set(self) -> int:
        """Get the accepting set."""
        return self._accepting_set

    @property
    def atom_type(self) -> AtomType:
        """Get the atom type."""
        return self._atom_type

    @property
    def accepting_sets(self) -> Set[int]:
        """Get the set of accepting sets."""
        return {self.accepting_set}

    def __str__(self):
        return str(self.atom_type.value) + "({})".format(self.accepting_set)


class Not(Atom):
    """This class implements a negation of an atom."""

    def __init__(self, accepting_set: int, atom_type: AtomType):
        """
        Initialize a negated.

        :param accepting_set: the accepting set (negated).
        :param atom_type: the type of the atom.
        """
        super().__init__(accepting_set, atom_type)

    @property
    def accepting_sets(self) -> Set[int]:
        """Get the set of accepting sets."""
        return {self.accepting_set}

    def __str__(self):
        return str(self.atom_type) + "(!{})".format(self.accepting_set)


class TrueAcceptance(AcceptanceCondition):
    """This class represent an "always accepting" condition."""

    def __str__(self):
        return "t"

    @property
    def accepting_sets(self) -> Set[int]:
        """Get the set of accepting sets."""
        return set()


class FalseAcceptance(AcceptanceCondition):
    """This class represent a "never accepting" condition."""

    def __str__(self):
        return "f"

    @property
    def accepting_sets(self) -> Set[int]:
        """Get the set of accepting sets."""
        return set()


class Acceptance:
    """This class represents the acceptance in the HOA format."""

    def __init__(self, condition: AcceptanceCondition, name: Optional[str] = None):
        """
        Initialize an acceptance.

        :param condition: the acceptance condition.
        :param name: (optional) the name for the acceptance.
        """
        self.condition = condition
        self.name = name

    def get_hoa_repr(self) -> str:
        """Get a compatible HOA format representation."""
        return "Acceptance: {} {}".format(self.condition.nb_accepting_sets, str(self.condition))


class LabelExpression(ABC):
    """This class implements a label expression."""

    @abstractmethod
    def __str__(self):
        """Transform the object to string."""

    @property
    @abstractmethod
    def propositions(self) -> Set[str]:
        """Get the set of all propositions."""


class AndLabelExpression(LabelExpression):
    """This class implements a conjunction between label expression."""

    def __init__(self, subexpressions: List[LabelExpression]):
        """
        Initialize the conjunction.

        :param subexpressions: the operands of the condition.
        """
        self._subexpressions = subexpressions

    @property
    def subexpressions(self) -> List[LabelExpression]:
        """Get the sub-expressions."""
        return self._subexpressions

    @property
    def propositions(self) -> Set[str]:
        """Get the set of all propositions."""
        return reduce(lambda x, y: x.union(y), map(lambda x: x.accepting_sets, self.subexpressions))

    def __str__(self):
        return " ".join(map(str, self.subexpressions))


class OrLabelExpression(LabelExpression):
    """This class implements a disjunction between label expression."""

    def __init__(self, subexpressions: List[LabelExpression]):
        """
        Initialize the conjunction.

        :param subexpressions: the operands of the condition.
        """
        self._subexpressions = subexpressions

    @property
    def subexpressions(self) -> List[LabelExpression]:
        """Get the sub-expressions."""
        return self._subexpressions

    @property
    def propositions(self) -> Set[str]:
        """Get the set of all propositions."""
        return reduce(lambda x, y: x.union(y), map(lambda x: x.accepting_sets, self.subexpressions))

    def __str__(self):
        return " ".join(map(str, self.subexpressions))


class AtomLabelExpression(LabelExpression):
    """This class implements an atom in a label expression."""

    def __init__(self, proposition: str):
        """
        Initialize an atom.

        :param proposition: the propositional symbol.
        """
        self._proposition = proposition

    @property
    def propositions(self) -> Set[str]:
        """Get the set of all propositions."""
        return {self._proposition}

    def __str__(self):
        return self._proposition


class NotLabelExpression(LabelExpression):
    """This class implements a negation of a label expression."""

    def __init__(self, subexpression: LabelExpression):
        """
        Initialize a negated label expression.

        :param subexpression: the label expression to negate.
        """
        self._subexpression = subexpression

    @property
    def subexpression(self) -> LabelExpression:
        """Get the subexpression."""
        return self._subexpression

    @property
    def propositions(self) -> Set[str]:
        """Get the set of all propositions."""
        return self.subexpression.propositions

    def __str__(self):
        return "!" + str(self.subexpression)


class AliasLabelExpression(LabelExpression):
    """This class implements an alias for a label expression."""

    def __init__(self, alias: str, expression: Optional[LabelExpression] = None):
        """
        Initialize the alias.

        :param alias: the alias for the label expression.
        :param expression: the aliased label expression (optional).
        """
        self._alias = alias
        self._expression = expression

    @property
    def expression(self) -> Optional[LabelExpression]:
        """Get the expression."""
        return self._expression

    @property
    def alias(self) -> str:
        """Get the alias."""
        return self._alias

    @property
    def propositions(self) -> Set[str]:
        """Ge the propositions."""
        assert self.expression is not None, "Cannot get propositions."
        return self.expression.propositions

    def __str__(self):
        return self.alias


class TrueLabelExpression(LabelExpression):
    """This class represent an "always accepting" condition."""

    def __str__(self):
        return "t"

    @property
    def propositions(self) -> Set[str]:
        """Get the set of all propositions."""
        return set()


class FalseLabelExpression(LabelExpression):
    """This class represent a "never accepting" condition."""

    def __str__(self):
        return "f"

    @property
    def propositions(self) -> Set[str]:
        """Get the set of all propositions."""
        return set()


class HOAHeader:
    """This class implements a data structure for the HOA file format header."""

    def __init__(self,
                 format_version: str,
                 acceptance: Acceptance,
                 nb_states: Optional[int] = None,
                 start_states: Optional[List[int]] = None,
                 aliases: Optional[List[AliasLabelExpression]] = None,
                 acceptance_name: Optional[str] = None,
                 propositions: Optional[Tuple[str]] = None,
                 tool: Optional[List[str]] = None,
                 name: Optional[str] = None,
                 properties: Optional[List[str]] = None,
                 headernames: Optional[Dict[str, List[str]]] = None):
        """
        Initialize a HOA header.

        :param format_version: the format version.
        :param nb_states: the number of states.
        :param start_states: the initial states.
        :param aliases: the list of aliases.
        :param acceptance_name: the acceptance name.
        :param acceptance: the acceptance condition.
        :param propositions: the propositions.
        :param tool: the tool property.
        :param name: the name property.
        :param properties: a list of properties.
        :param headernames: a dictionary of additional header-names.
        """
        self._format_version = format_version
        self._acceptance = acceptance
        self._nb_states = nb_states
        self._start_states = start_states
        self._aliases = aliases
        self._acceptance_name = acceptance_name
        self._propositions = propositions
        self._tool = tool
        self._name = name
        self._properties = properties
        self._headernames = headernames

    @property
    def format_version(self) -> str:
        """Get the 'format_version' property."""
        return self._format_version

    @property
    def nb_states(self) -> Optional[int]:
        """Get the 'nb_states' property."""
        return self._nb_states

    @property
    def start_states(self) -> Optional[List[int]]:
        """Get the 'start_state' property."""
        return self._start_states

    @property
    def aliases(self) -> Optional[List[AliasLabelExpression]]:
        """Get the 'aliases' property."""
        return self._start_states

    @property
    def acceptance_name(self) -> Optional[str]:
        """Get the 'acceptance_name' property."""
        return self._acceptance_name

    @property
    def acceptance(self) -> Acceptance:
        """Get the 'acceptance' property."""
        return self._acceptance

    @property
    def propositions(self) -> Optional[Tuple[str]]:
        """Get the 'propositions' property."""
        return self._propositions

    @property
    def tool(self) -> Optional[List[str]]:
        """Get the tool property."""
        return self._tool

    @property
    def name(self) -> Optional[str]:
        """Get the name property."""
        return self._name

    @property
    def properties(self) -> Optional[List[str]]:
        """Get the properties."""
        return self._properties

    @property
    def headernames(self) -> Optional[Dict[str, List[str]]]:
        """Get the headernames."""
        return self._headernames

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
            s += "AP: {nb} {prop}\n".format(nb=len(self.propositions), prop=propositions_string)
        if self.aliases is not None and len(self.aliases) > 0:
            s += "\n".join(["Alias: {}".format(str(alias)) for alias in self.aliases]) + "\n"
        if self.acceptance_name is not None:
            s += "acc-name: {}\n".format(self.acceptance_name)
        s += self.acceptance.get_hoa_repr() + "\n"
        if self.tool is not None:
            s += "tool: {}\n".format(" ".join(self.tool))
        if self.name is not None:
            s += "name: {}\n".format(self.name)
        if self.properties is not None and len(self.properties) > 0:
            s += "properties: {}\n".format(" ".join(self.properties))
        if self.headernames is not None and len(self.headernames) > 0:
            s += "\n".join(["{}: {}".format(key, " ".join(values)) for key, values in self.headernames.items()]) + "\n"

        return s

class HOABody:
    """This class implements a data structure for the HOA file format header."""

    def dumps(self) -> str:
        """
        Dump the body data into a string in HOA format.

        :return: the body string in HOA format.
        """
        return ""


class HOA:
    """This class implements a data structure for the HOA file format."""

    def __init__(self, header: HOAHeader, body: HOABody):
        """
        Initialize the HOA data structure.

        :param header: the header of the HOA file.
        :param body: the body of the HOA file.
        """
        self.header = header
        self.body = body

    def dump(self, filepath: PathLike) -> None:
        """
        Dump the data to a file.

        :param filepath: the path to the file.
        :return: None.
        """
        raise NotImplementedError

    def dumps(self) -> str:
        """
        Dump the data into a string in HOA format.

        :return: the string in HOA format.
        """
        header = self.header.dumps()
        body = self.body.dumps()
        return header + "--BODY--" + body + "--END--"
