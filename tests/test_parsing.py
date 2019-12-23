# -*- coding: utf-8 -*-
"""Test the parsing module."""
from pathlib import Path
from collections import OrderedDict

from hoa2dot.core import HOA, Acceptance, Atom, AtomType, And, TrueAcceptance, AliasLabelExpression, \
    AtomLabelExpression, AndLabelExpression, NotLabelExpression, State, Edge, TrueLabelExpression
from hoa2dot.parsers import HOAParser

from .conftest import CUR_PATH


class TestParsingAut1:
    """Test parsing for tests/examples/aut1."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj = parser(open(str(Path(CUR_PATH, "examples", "aut1.hoa"))).read())  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_format_version(self):
        """Test that the format version is correct."""
        assert self.hoa_header.format_version == "v1"

    def test_nb_states(self):
        """Test that the number of states is correct."""
        assert self.hoa_header.nb_states == 2

    def test_start_states(self):
        """Test that the initial states are correct."""
        assert self.hoa_header.start_states == [0]

    def test_acc_name(self):
        """Test that the acc-name is correct."""
        assert self.hoa_header.acceptance_name == "Rabin 1"

    def test_acceptance(self):
        """Test that the acceptance condition is correct."""
        assert self.hoa_header.acceptance.condition.nb_accepting_sets == 2
        assert self.hoa_header.acceptance == Acceptance(And([Atom(0, AtomType.FINITE), Atom(1, AtomType.INFINITE),
                                                             TrueAcceptance()]))

    def test_AP(self):
        """Test that AP is correct."""
        assert self.hoa_header.propositions == ('a', 'b')
        assert len(self.hoa_header.propositions) == 2

    def test_aliases(self):
        """Test that Alias is correct."""
        assert self.hoa_header.aliases[0] == AliasLabelExpression('@a', AtomLabelExpression("0"))
        assert self.hoa_header.aliases[1] == AliasLabelExpression('@b', AtomLabelExpression("1"))

    def test_body(self):
        """Test that the HOA body is correct."""
        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0, None, '"a U b"', None)] = [Edge([0], AndLabelExpression([AtomLabelExpression("0"),
                                                                                           NotLabelExpression(
                                                                                               AtomLabelExpression("1"))
                                                                                           ]), {0}),
                                                             Edge([1], AtomLabelExpression("1"), {0})]
        state_edges_dict[State(1, None, None, None)] = [Edge([1], TrueLabelExpression(), {1})]
        assert self.hoa_body.state2edges == state_edges_dict


class TestParsingAut2:
    """Test parsing for tests/examples/aut2."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj = parser(open(str(Path(CUR_PATH, "examples", "aut2.hoa"))).read())  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_format_version(self):
        """Test that the format version is correct."""
        assert self.hoa_header.format_version == "v1"

    def test_nb_states(self):
        """Test that the number of states is correct."""
        assert self.hoa_header.nb_states == 3

    def test_start_states(self):
        """Test that the initial states are correct."""
        assert self.hoa_header.start_states == [0]

    def test_acc_name(self):
        """Test that the acc-name is correct."""
        assert self.hoa_header.acceptance_name == "Rabin 1"

    def test_acceptance(self):
        """Test that the acceptance condition is correct."""
        assert self.hoa_header.acceptance.condition.nb_accepting_sets == 2
        assert self.hoa_header.acceptance == Acceptance(And([Atom(0, AtomType.FINITE), Atom(1, AtomType.INFINITE)]))

    def test_AP(self):
        """Test that AP is correct."""
        assert self.hoa_header.propositions == ('a', 'b')
        assert len(self.hoa_header.propositions) == 2

    def test_body(self):
        """Test that the HOA body is correct."""
        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0, None, '"a U b"', {0})] = [Edge([2], None, None), Edge([0], None, None),
                                                            Edge([1], None, None), Edge([1], None, None)]

        state_edges_dict[State(1, None, None, {1})] = [Edge([1], None, None), Edge([1], None, None),
                                                       Edge([1], None, None), Edge([1], None, None)]
        state_edges_dict[State(2, None, '"sink state"', {0})] = [Edge([2], None, None), Edge([2], None, None),
                                                                 Edge([2], None, None), Edge([2], None, None)]

        assert self.hoa_body.state2edges == state_edges_dict
