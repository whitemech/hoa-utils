# -*- coding: utf-8 -*-
"""Test the parsing module."""
import os
import tempfile
from pathlib import Path
from collections import OrderedDict

import pytest

from hoa2dot.core import HOA, Acceptance, Atom, AtomType, And, TrueAcceptance, AliasLabelExpression, \
    AtomLabelExpression, AndLabelExpression, NotLabelExpression, State, Edge, TrueLabelExpression, HOABody
from hoa2dot.parsers import HOAParser

from .conftest import TEST_ROOT_DIR


@pytest.mark.parametrize(
    ["filepath"],
    [
        (os.path.join(TEST_ROOT_DIR, "examples", "aut1.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut2.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut3.2.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut3.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut4.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut5.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut6.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut7.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut8.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut11.hoa"),)
    ]
)
def test_parsing_is_deterministic(filepath):
    """Test that parsing is deterministic."""
    parser = HOAParser()
    hoa_obj_1 = parser(open(filepath).read())  # type: HOA
    temp = tempfile.mktemp()
    hoa_obj_1.dump(open(temp, "w"))
    hoa_obj_2 = parser(open(temp).read())
    assert hoa_obj_1 == hoa_obj_2


class TestParsingAut1:
    """Test parsing for tests/examples/aut1."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj = parser(open(str(Path(TEST_ROOT_DIR, "examples", "aut1.hoa"))).read())  # type: HOA
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
        state_edges_dict[State(0, name="a U b")] = [Edge([0], AndLabelExpression([AtomLabelExpression("0"),
                                                                                  NotLabelExpression(
                                                                                      AtomLabelExpression("1"))]),
                                                         frozenset({0})), Edge([1], AtomLabelExpression("1"),
                                                                               frozenset({0}))]
        state_edges_dict[State(1)] = [Edge([1], TrueLabelExpression(), frozenset({1}))]
        assert self.hoa_body.state2edges == state_edges_dict


class TestParsingAut2:
    """Test parsing for tests/examples/aut2."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj = parser(open(str(Path(TEST_ROOT_DIR, "examples", "aut3.2.hoa"))).read())  # type: HOA
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
        state_edges_dict[State(0, name="a U b", acc_sig=frozenset({0}))] = [Edge([2]), Edge([0]), Edge([1]),
                                                                            Edge([1])]

        state_edges_dict[State(1, acc_sig=frozenset({1}))] = [Edge([1]), Edge([1]), Edge([1]), Edge([1])]
        state_edges_dict[State(2, name="sink state", acc_sig=frozenset({0}))] = [Edge([2]), Edge([2]), Edge([2]),
                                                                                 Edge([2])]

        assert self.hoa_body.state2edges == state_edges_dict
