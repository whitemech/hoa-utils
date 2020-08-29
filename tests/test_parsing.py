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

"""Test the parsing module."""
import os
from collections import OrderedDict
from io import StringIO
from pathlib import Path

import pytest

from hoa.ast.acceptance import Fin, Inf, nb_accepting_sets
from hoa.ast.boolean_expression import TRUE
from hoa.ast.label import LabelAlias, LabelAtom, propositions
from hoa.core import Acceptance, Edge, HOA, HOABody, HOAHeader, State
from hoa.dumpers import dump
from hoa.parsers import HOAParser
from hoa.types import alias, identifier, proposition, string

from .conftest import HOA_FILES, TEST_ROOT_DIR


@pytest.mark.parametrize(
    "filepath",
    HOA_FILES,
)
def test_parsing_is_deterministic(filepath):
    """Test that parsing is deterministic."""
    parser = HOAParser()
    hoa_obj_1 = parser(open(filepath).read())  # type: HOA
    temp = StringIO()
    dump(hoa_obj_1, temp)
    temp.seek(0)
    hoa_obj_2 = parser(temp.read())
    assert hoa_obj_1 == hoa_obj_2


class TestParsingAut1:
    """Test parsing for tests/examples/aut1."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj: HOA = parser(
            Path(TEST_ROOT_DIR, "examples", "aut1.hoa").read_text()
        )
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
        assert self.hoa_header.start_states == {frozenset([0])}

    def test_acc_name(self):
        """Test that the acc-name is correct."""
        assert self.hoa_header.acceptance.name == "Rabin"

    def test_acceptance(self):
        """Test that the acceptance condition is correct."""
        assert nb_accepting_sets(self.hoa_header.acceptance.condition) == 2
        assert self.hoa_header.acceptance == Acceptance(
            Fin(0) & Inf(1) & TRUE, identifier("Rabin"), (1,)
        )

    def test_AP(self):
        """Test that AP is correct."""
        assert self.hoa_header.propositions == ("a", "b")
        assert len(self.hoa_header.propositions) == 2

    def test_aliases(self):
        """Test that Alias is correct."""
        assert self.hoa_header.aliases[0] == LabelAlias(alias("@a"), LabelAtom(0))
        assert self.hoa_header.aliases[1] == LabelAlias(alias("@b"), LabelAtom(1))

    def test_body(self):
        """Test that the HOA body is correct."""
        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0, name=string("a U b"))] = [
            Edge(
                [0],
                LabelAtom(0) & ~LabelAtom(1),
                {0},
            ),
            Edge([1], LabelAtom(1), {0}),
        ]
        state_edges_dict[State(1)] = [Edge([1], TRUE, {1})]
        assert self.hoa_body.state2edges == state_edges_dict


class TestParsingAut2:
    """Test parsing for tests/examples/aut2."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj: HOA = parser(
            Path(TEST_ROOT_DIR, "examples", "aut2.hoa").read_text()
        )
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
        assert self.hoa_header.start_states == {frozenset({0})}

    def test_acc_name(self):
        """Test that the acc-name is correct."""
        assert self.hoa_header.acceptance.name == "Rabin"

    def test_acceptance(self):
        """Test that the acceptance condition is correct."""
        assert nb_accepting_sets(self.hoa_header.acceptance.condition) == 2
        assert self.hoa_header.acceptance == Acceptance(
            Fin(0) & Inf(1), identifier("Rabin"), (1,)
        )

    def test_AP(self):
        """Test that AP is correct."""
        assert self.hoa_header.propositions == ("a", "b")

    def test_body(self):
        """Test that the HOA body is correct."""
        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0, name=string("a U b"), acc_sig=frozenset({0}))] = [
            Edge([2]),
            Edge([0]),
            Edge([1]),
            Edge([1]),
        ]

        state_edges_dict[State(1, acc_sig=frozenset({1}))] = [
            Edge([1]),
            Edge([1]),
            Edge([1]),
            Edge([1]),
        ]
        state_edges_dict[
            State(2, name=string("sink state"), acc_sig=frozenset({0}))
        ] = [
            Edge([2]),
            Edge([2]),
            Edge([2]),
            Edge([2]),
        ]

        assert self.hoa_body.state2edges == state_edges_dict


class TestParsingAut3:
    """Test parsing for tests/examples/aut3."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj: HOA = parser(
            Path(TEST_ROOT_DIR, "examples", "aut3.hoa").read_text()
        )
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_hoa_header(self):
        """Test that the HOA header is correct."""
        hoa_header = HOAHeader(
            identifier("v1"),
            acceptance=Acceptance(
                Inf(0) & Inf(1), identifier("generalized-Buchi"), (2,)
            ),
            nb_states=1,
            start_states={frozenset([0])},
            propositions=(string("a"), string("b")),
            name=string("GFa & GFb"),
        )
        assert self.hoa_header == hoa_header

    def test_hoa_body(self):
        """Test that the HOA body is correct."""
        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0)] = [
            Edge([0]),
            Edge([0], acc_sig=frozenset({0})),
            Edge([0], acc_sig=frozenset({1})),
            Edge([0], acc_sig=frozenset({0, 1})),
        ]
        hoa_body = HOABody(state_edges_dict)
        assert self.hoa_body == hoa_body


class TestParsingAut3_2:
    """Test parsing for tests/examples/aut3.2."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj: HOA = parser(
            Path(TEST_ROOT_DIR, "examples", "aut3.2.hoa").read_text()
        )
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_hoa_header(self):
        """Test that the HOA header is correct."""
        hoa_header = HOAHeader(
            identifier("v1"),
            Acceptance(Inf(0) & Inf(1), identifier("generalized-Buchi"), (2,)),
            nb_states=1,
            start_states={frozenset([0])},
            propositions=(string("a"), string("b")),
            name=string("GFa & GFb"),
        )
        assert self.hoa_header == hoa_header

    def test_hoa_body(self):
        """Test that the HOA body is correct."""
        a0, a1 = LabelAtom(0), LabelAtom(1)
        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0)] = [
            Edge(
                [0],
                label=~a0 & ~a1,
            ),
            Edge(
                [0],
                label=a0 & ~a1,
                acc_sig={0},
            ),
            Edge(
                [0],
                label=~a0 & a1,
                acc_sig={1},
            ),
            Edge(
                [0],
                label=a0 & a1,
                acc_sig={0, 1},
            ),
        ]
        hoa_body = HOABody(state_edges_dict)
        assert self.hoa_body == hoa_body


class TestParsingAut4:
    """Test parsing for tests/examples/aut4."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj = parser(
            Path(TEST_ROOT_DIR, "examples", "aut4.hoa").read_text()
        )  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

        cls.alias_a = LabelAlias(alias("@a"), LabelAtom(0))
        cls.alias_b = LabelAlias(alias("@bc"), LabelAtom(1) & LabelAtom(2))

    def test_hoa_header(self):
        """Test that the HOA header is correct."""
        hoa_header = HOAHeader(
            identifier("v1"),
            Acceptance(Inf(0) & Inf(1), identifier("generalized-Buchi"), (2,)),
            nb_states=1,
            start_states={frozenset([0])},
            propositions=(string("a"), string("b"), string("c")),
            name=string("GFa & GF(b & c)"),
            aliases=[
                self.alias_a,
                self.alias_b,
            ],
        )
        assert self.hoa_header == hoa_header

    def test_hoa_body(self):
        """Test that the HOA body is correct."""
        state_edges_dict = OrderedDict({})
        hoa_body = HOABody(state_edges_dict)
        state_edges_dict[State(0)] = [
            Edge(
                [0],
                label=~self.alias_a & ~self.alias_b,
            ),
            Edge(
                [0],
                label=self.alias_a & ~self.alias_b,
                acc_sig={0},
            ),
            Edge(
                [0],
                label=~self.alias_a & self.alias_b,
                acc_sig={1},
            ),
            Edge(
                [0],
                label=self.alias_a & self.alias_b,
                acc_sig={0, 1},
            ),
        ]
        assert self.hoa_body == hoa_body


class TestParsingAut5:
    """Test parsing for tests/examples/aut5."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj = parser(
            Path(TEST_ROOT_DIR, "examples", "aut5.hoa").read_text()
        )  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_hoa_header(self):
        """Test that the HOA header is correct."""
        hoa_header = HOAHeader(
            identifier("v1"),
            Acceptance(Inf(0), identifier("Buchi")),
            nb_states=2,
            start_states={frozenset([0]), frozenset([1])},
            propositions=(string("a"),),
            name=string("GFa"),
        )
        assert self.hoa_header == hoa_header

    def test_hoa_body(self):
        """Test that the HOA body is correct."""
        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0, label=LabelAtom(0), acc_sig=frozenset({0}))] = [
            Edge([0]),
            Edge([1]),
        ]
        state_edges_dict[State(1, label=~LabelAtom(0))] = [
            Edge([0]),
            Edge([1]),
        ]
        hoa_body = HOABody(state_edges_dict)
        assert self.hoa_body == hoa_body


class TestParsingAut6:
    """Test parsing for tests/examples/aut6."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj = parser(
            Path(TEST_ROOT_DIR, "examples", "aut6.hoa").read_text()
        )  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_hoa(self):
        """Test that the HOA automaton is correct."""
        hoa_header = HOAHeader(
            identifier("v1"),
            Acceptance(Inf(0), identifier("Buchi")),
            nb_states=3,
            start_states={frozenset([0])},
            propositions=(string("a"),),
        )

        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0)] = [
            Edge([1], label=LabelAtom(0)),
            Edge([2], label=~(LabelAtom(0))),
        ]
        state_edges_dict[State(1)] = [
            Edge([1], label=LabelAtom(0), acc_sig=frozenset({0})),
            Edge(
                [2],
                label=~(LabelAtom(0)),
                acc_sig=frozenset({0}),
            ),
        ]
        state_edges_dict[State(2)] = [
            Edge([1], label=LabelAtom(0)),
            Edge([2], label=~LabelAtom(0)),
        ]
        hoa_body = HOABody(state_edges_dict)

        hoa_obj = HOA(hoa_header, hoa_body)
        assert self.hoa_obj == hoa_obj


class TestParsingAut7:
    """Test parsing for tests/examples/aut7."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj = parser(
            Path(TEST_ROOT_DIR, "examples", "aut7.hoa").read_text()
        )  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_hoa(self):
        """Test that the HOA automaton is correct."""
        hoa_header = HOAHeader(
            identifier("v1"),
            Acceptance(Inf(0), identifier("Buchi")),
            start_states={frozenset([0])},
            propositions=(string("a"), string("b")),
            name=string("GFa | G(b <-> Xa)"),
            properties=[identifier("explicit-labels"), identifier("trans-labels")],
        )

        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0)] = [
            Edge([1], label=TRUE),
            Edge([2], label=LabelAtom(1)),
            Edge([3], label=~LabelAtom(1)),
        ]
        state_edges_dict[State(1, name=string("GFa"))] = [
            Edge([1], label=LabelAtom(0), acc_sig=frozenset({0})),
            Edge([1], label=~LabelAtom(0)),
        ]
        state_edges_dict[
            State(2, name=string("a & G(b <-> Xa)"), acc_sig=frozenset({0}))
        ] = [
            Edge(
                [2],
                label=LabelAtom(0) & LabelAtom(1),
            ),
            Edge([3], label=LabelAtom(0) & ~(LabelAtom(1))),
        ]
        state_edges_dict[
            State(3, name=string("!a & G(b <-> Xa)"), acc_sig=frozenset({0}))
        ] = [
            Edge(
                [2],
                label=~(LabelAtom(0)) & LabelAtom(1),
            ),
            Edge(
                [3],
                label=~(LabelAtom(0)) & ~LabelAtom(1),
            ),
        ]
        hoa_body = HOABody(state_edges_dict)

        hoa_obj = HOA(hoa_header, hoa_body)
        assert self.hoa_obj == hoa_obj


class TestParsingAut8:
    """Test parsing for tests/examples/aut8."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj = parser(
            Path(TEST_ROOT_DIR, "examples", "aut8.hoa").read_text()
        )  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_hoa(self):
        """Test that the HOA automaton is correct."""
        hoa_header = HOAHeader(
            identifier("v1"),
            Acceptance(Inf(0), identifier("Buchi")),
            start_states={frozenset([0])},
            propositions=(string("a"), string("b")),
            name=string("GFa | G(b <-> Xa)"),
            properties=[
                identifier("explicit-labels"),
                identifier("trans-labels"),
                identifier("trans-acc"),
            ],
        )

        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0)] = [
            Edge([1], label=TRUE),
            Edge([2], label=LabelAtom(1)),
            Edge([3], label=~(LabelAtom(1))),
        ]
        state_edges_dict[State(1, name=string("GFa"))] = [
            Edge([1], label=LabelAtom(0), acc_sig=frozenset({0})),
            Edge([1], label=~(LabelAtom(0))),
        ]
        state_edges_dict[State(2, name=string("a & G(b <-> Xa)"))] = [
            Edge(
                [2],
                label=LabelAtom(0) & LabelAtom(1),
                acc_sig=frozenset({0}),
            ),
            Edge(
                [3],
                label=LabelAtom(0) & ~LabelAtom(1),
                acc_sig=frozenset({0}),
            ),
        ]
        state_edges_dict[State(3, name=string("!a & G(b <-> Xa)"))] = [
            Edge(
                [2],
                label=~LabelAtom(0) & LabelAtom(1),
                acc_sig=frozenset({0}),
            ),
            Edge(
                [3],
                label=~LabelAtom(0) & ~LabelAtom(1),
                acc_sig=frozenset({0}),
            ),
        ]
        hoa_body = HOABody(state_edges_dict)

        hoa_obj = HOA(hoa_header, hoa_body)
        assert self.hoa_obj == hoa_obj


class TestParsingAut11:
    """Test parsing for tests/examples/aut11."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj: HOA = parser(
            Path(TEST_ROOT_DIR, "examples", "aut11.hoa").read_text()
        )
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_hoa(self):
        """Test that the HOA automaton is correct."""
        hoa_header = HOAHeader(
            identifier("v1"),
            Acceptance(Fin(0), identifier("co-Buchi")),
            nb_states=4,
            start_states={frozenset([0, 2]), frozenset([3])},
            propositions=(string("a"), string("b"), string("c")),
            name=string("(Fa & G(b&Xc)) | c"),
        )

        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0, name=string("Fa"))] = [
            Edge([0], label=TRUE, acc_sig=frozenset({0})),
            Edge([1], label=LabelAtom(0)),
        ]
        state_edges_dict[State(1, name=string("true"))] = [Edge([1], label=TRUE)]
        state_edges_dict[State(2, name=string("G(b&Xc)"))] = [
            Edge([2, 3], label=LabelAtom(1))
        ]
        state_edges_dict[State(3, name=string("c"))] = [Edge([1], label=LabelAtom(2))]
        hoa_body = HOABody(state_edges_dict)

        hoa_obj = HOA(hoa_header, hoa_body)
        assert self.hoa_obj == hoa_obj
