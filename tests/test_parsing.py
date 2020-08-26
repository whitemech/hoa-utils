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
import tempfile
from collections import OrderedDict
from pathlib import Path

import pytest

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
    HOABody,
    HOAHeader,
    NotLabelExpression,
    State,
    TrueAcceptance,
    TrueLabelExpression,
)
from hoa2dot.parsers import HOAParser

from .conftest import TEST_ROOT_DIR


@pytest.mark.parametrize(
    ["filepath"],
    [
        (os.path.join(TEST_ROOT_DIR, "examples", "aut1.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut2.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut3.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut3.2.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut4.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut5.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut6.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut7.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut8.hoa"),),
        (os.path.join(TEST_ROOT_DIR, "examples", "aut11.hoa"),),
    ],
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
        cls.hoa_obj = parser(
            open(str(Path(TEST_ROOT_DIR, "examples", "aut1.hoa"))).read()
        )  # type: HOA
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
        assert self.hoa_header.acceptance == Acceptance(
            And(
                [Atom(0, AtomType.FINITE), Atom(1, AtomType.INFINITE), TrueAcceptance()]
            )
        )

    def test_AP(self):
        """Test that AP is correct."""
        assert self.hoa_header.propositions == ("a", "b")
        assert len(self.hoa_header.propositions) == 2

    def test_aliases(self):
        """Test that Alias is correct."""
        assert self.hoa_header.aliases[0] == AliasLabelExpression(
            "@a", AtomLabelExpression("0")
        )
        assert self.hoa_header.aliases[1] == AliasLabelExpression(
            "@b", AtomLabelExpression("1")
        )

    def test_body(self):
        """Test that the HOA body is correct."""
        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0, name="a U b")] = [
            Edge(
                [0],
                AndLabelExpression(
                    [
                        AtomLabelExpression("0"),
                        NotLabelExpression(AtomLabelExpression("1")),
                    ]
                ),
                frozenset({0}),
            ),
            Edge([1], AtomLabelExpression("1"), frozenset({0})),
        ]
        state_edges_dict[State(1)] = [Edge([1], TrueLabelExpression(), frozenset({1}))]
        assert self.hoa_body.state2edges == state_edges_dict


class TestParsingAut2:
    """Test parsing for tests/examples/aut2."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj = parser(
            open(str(Path(TEST_ROOT_DIR, "examples", "aut2.hoa"))).read()
        )  # type: HOA
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
        assert self.hoa_header.acceptance == Acceptance(
            And([Atom(0, AtomType.FINITE), Atom(1, AtomType.INFINITE)])
        )

    def test_AP(self):
        """Test that AP is correct."""
        assert self.hoa_header.propositions == ("a", "b")
        assert len(self.hoa_header.propositions) == 2

    def test_body(self):
        """Test that the HOA body is correct."""
        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0, name="a U b", acc_sig=frozenset({0}))] = [
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
        state_edges_dict[State(2, name="sink state", acc_sig=frozenset({0}))] = [
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
        cls.hoa_obj = parser(
            open(str(Path(TEST_ROOT_DIR, "examples", "aut3.hoa"))).read()
        )  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_hoa_header(self):
        """Test that the HOA header is correct."""
        hoa_header = HOAHeader(
            "v1",
            Acceptance(And([Atom(0, AtomType.INFINITE), Atom(1, AtomType.INFINITE)])),
            nb_states=1,
            start_states=[0],
            acceptance_name="generalized-Buchi 2",
            propositions=("a", "b"),
            name="GFa & GFb",
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
        cls.hoa_obj = parser(
            open(str(Path(TEST_ROOT_DIR, "examples", "aut3.2.hoa"))).read()
        )  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_hoa_header(self):
        """Test that the HOA header is correct."""
        hoa_header = HOAHeader(
            "v1",
            Acceptance(And([Atom(0, AtomType.INFINITE), Atom(1, AtomType.INFINITE)])),
            nb_states=1,
            start_states=[0],
            acceptance_name="generalized-Buchi 2",
            propositions=("a", "b"),
            name="GFa & GFb",
        )
        assert self.hoa_header == hoa_header

    def test_hoa_body(self):
        """Test that the HOA body is correct."""
        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0)] = [
            Edge(
                [0],
                label=AndLabelExpression(
                    [
                        NotLabelExpression(AtomLabelExpression("0")),
                        NotLabelExpression(AtomLabelExpression("1")),
                    ]
                ),
            ),
            Edge(
                [0],
                label=AndLabelExpression(
                    [
                        AtomLabelExpression("0"),
                        NotLabelExpression(AtomLabelExpression("1")),
                    ]
                ),
                acc_sig=frozenset({0}),
            ),
            Edge(
                [0],
                label=AndLabelExpression(
                    [
                        NotLabelExpression(AtomLabelExpression("0")),
                        AtomLabelExpression("1"),
                    ]
                ),
                acc_sig=frozenset({1}),
            ),
            Edge(
                [0],
                label=AndLabelExpression(
                    [AtomLabelExpression("0"), AtomLabelExpression("1")]
                ),
                acc_sig=frozenset({0, 1}),
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
            open(str(Path(TEST_ROOT_DIR, "examples", "aut4.hoa"))).read()
        )  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_hoa_header(self):
        """Test that the HOA header is correct."""
        hoa_header = HOAHeader(
            "v1",
            Acceptance(And([Atom(0, AtomType.INFINITE), Atom(1, AtomType.INFINITE)])),
            nb_states=1,
            start_states=[0],
            acceptance_name="generalized-Buchi 2",
            propositions=("a", "b", "c"),
            name="GFa & GF(b & c)",
            aliases=[
                AliasLabelExpression("@a", AtomLabelExpression("0")),
                AliasLabelExpression(
                    "@bc",
                    AndLabelExpression(
                        [AtomLabelExpression("1"), AtomLabelExpression("2")]
                    ),
                ),
            ],
        )
        assert self.hoa_header == hoa_header

    def test_hoa_body(self):
        """Test that the HOA body is correct."""
        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0)] = [
            Edge(
                [0],
                label=AndLabelExpression(
                    [
                        NotLabelExpression(AliasLabelExpression("@a")),
                        NotLabelExpression(AliasLabelExpression("@bc")),
                    ]
                ),
            ),
            Edge(
                [0],
                label=AndLabelExpression(
                    [
                        AliasLabelExpression("@a"),
                        NotLabelExpression(AliasLabelExpression("@bc")),
                    ]
                ),
                acc_sig=frozenset({0}),
            ),
            Edge(
                [0],
                label=AndLabelExpression(
                    [
                        NotLabelExpression(AliasLabelExpression("@a")),
                        AliasLabelExpression("@bc"),
                    ]
                ),
                acc_sig=frozenset({1}),
            ),
            Edge(
                [0],
                label=AndLabelExpression(
                    [AliasLabelExpression("@a"), AliasLabelExpression("@bc")]
                ),
                acc_sig=frozenset({0, 1}),
            ),
        ]
        hoa_body = HOABody(state_edges_dict)
        assert self.hoa_body == hoa_body


class TestParsingAut5:
    """Test parsing for tests/examples/aut5."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj = parser(
            open(str(Path(TEST_ROOT_DIR, "examples", "aut5.hoa"))).read()
        )  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_hoa_header(self):
        """Test that the HOA header is correct."""
        hoa_header = HOAHeader(
            "v1",
            Acceptance(Atom(0, AtomType.INFINITE)),
            nb_states=2,
            start_states=[0, 1],
            acceptance_name="Buchi",
            propositions=("a",),
            name="GFa",
        )
        assert self.hoa_header == hoa_header

    def test_hoa_body(self):
        """Test that the HOA body is correct."""
        state_edges_dict = OrderedDict({})
        state_edges_dict[
            State(0, label=AtomLabelExpression("0"), acc_sig=frozenset({0}))
        ] = [Edge([0]), Edge([1])]
        state_edges_dict[
            State(1, label=NotLabelExpression(AtomLabelExpression("0")))
        ] = [Edge([0]), Edge([1])]
        hoa_body = HOABody(state_edges_dict)
        assert self.hoa_body == hoa_body


class TestParsingAut6:
    """Test parsing for tests/examples/aut6."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj = parser(
            open(str(Path(TEST_ROOT_DIR, "examples", "aut6.hoa"))).read()
        )  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_hoa(self):
        """Test that the HOA automaton is correct."""
        hoa_header = HOAHeader(
            "v1",
            Acceptance(Atom(0, AtomType.INFINITE)),
            nb_states=3,
            start_states=[0],
            acceptance_name="Buchi",
            propositions=("a",),
        )

        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0)] = [
            Edge([1], label=AtomLabelExpression("0")),
            Edge([2], label=NotLabelExpression(AtomLabelExpression("0"))),
        ]
        state_edges_dict[State(1)] = [
            Edge([1], label=AtomLabelExpression("0"), acc_sig=frozenset({0})),
            Edge(
                [2],
                label=NotLabelExpression(AtomLabelExpression("0")),
                acc_sig=frozenset({0}),
            ),
        ]
        state_edges_dict[State(2)] = [
            Edge([1], label=AtomLabelExpression("0")),
            Edge([2], label=NotLabelExpression(AtomLabelExpression("0"))),
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
            open(str(Path(TEST_ROOT_DIR, "examples", "aut7.hoa"))).read()
        )  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_hoa(self):
        """Test that the HOA automaton is correct."""
        hoa_header = HOAHeader(
            "v1",
            Acceptance(Atom(0, AtomType.INFINITE)),
            start_states=[0],
            acceptance_name="Buchi",
            propositions=("a", "b"),
            name="GFa | G(b <-> Xa)",
            properties=["explicit-labels", "trans-labels"],
        )

        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0)] = [
            Edge([1], label=TrueLabelExpression()),
            Edge([2], label=AtomLabelExpression("1")),
            Edge([3], label=NotLabelExpression(AtomLabelExpression("1"))),
        ]
        state_edges_dict[State(1, name="GFa")] = [
            Edge([1], label=AtomLabelExpression("0"), acc_sig=frozenset({0})),
            Edge([1], label=NotLabelExpression(AtomLabelExpression("0"))),
        ]
        state_edges_dict[State(2, name="a & G(b <-> Xa)", acc_sig=frozenset({0}))] = [
            Edge(
                [2],
                label=AndLabelExpression(
                    [AtomLabelExpression("0"), AtomLabelExpression("1")]
                ),
            ),
            Edge(
                [3],
                label=AndLabelExpression(
                    [
                        AtomLabelExpression("0"),
                        NotLabelExpression(AtomLabelExpression("1")),
                    ]
                ),
            ),
        ]
        state_edges_dict[State(3, name="!a & G(b <-> Xa)", acc_sig=frozenset({0}))] = [
            Edge(
                [2],
                label=AndLabelExpression(
                    [
                        NotLabelExpression(AtomLabelExpression("0")),
                        AtomLabelExpression("1"),
                    ]
                ),
            ),
            Edge(
                [3],
                label=AndLabelExpression(
                    [
                        NotLabelExpression(AtomLabelExpression("0")),
                        NotLabelExpression(AtomLabelExpression("1")),
                    ]
                ),
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
            open(str(Path(TEST_ROOT_DIR, "examples", "aut8.hoa"))).read()
        )  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_hoa(self):
        """Test that the HOA automaton is correct."""
        hoa_header = HOAHeader(
            "v1",
            Acceptance(Atom(0, AtomType.INFINITE)),
            start_states=[0],
            acceptance_name="Buchi",
            propositions=("a", "b"),
            name="GFa | G(b <-> Xa)",
            properties=["explicit-labels", "trans-labels", "trans-acc"],
        )

        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0)] = [
            Edge([1], label=TrueLabelExpression()),
            Edge([2], label=AtomLabelExpression("1")),
            Edge([3], label=NotLabelExpression(AtomLabelExpression("1"))),
        ]
        state_edges_dict[State(1, name="GFa")] = [
            Edge([1], label=AtomLabelExpression("0"), acc_sig=frozenset({0})),
            Edge([1], label=NotLabelExpression(AtomLabelExpression("0"))),
        ]
        state_edges_dict[State(2, name="a & G(b <-> Xa)")] = [
            Edge(
                [2],
                label=AndLabelExpression(
                    [AtomLabelExpression("0"), AtomLabelExpression("1")]
                ),
                acc_sig=frozenset({0}),
            ),
            Edge(
                [3],
                label=AndLabelExpression(
                    [
                        AtomLabelExpression("0"),
                        NotLabelExpression(AtomLabelExpression("1")),
                    ]
                ),
                acc_sig=frozenset({0}),
            ),
        ]
        state_edges_dict[State(3, name="!a & G(b <-> Xa)")] = [
            Edge(
                [2],
                label=AndLabelExpression(
                    [
                        NotLabelExpression(AtomLabelExpression("0")),
                        AtomLabelExpression("1"),
                    ]
                ),
                acc_sig=frozenset({0}),
            ),
            Edge(
                [3],
                label=AndLabelExpression(
                    [
                        NotLabelExpression(AtomLabelExpression("0")),
                        NotLabelExpression(AtomLabelExpression("1")),
                    ]
                ),
                acc_sig=frozenset({0}),
            ),
        ]
        hoa_body = HOABody(state_edges_dict)

        hoa_obj = HOA(hoa_header, hoa_body)
        assert self.hoa_obj == hoa_obj


class TestParsingAut11:
    """Test parsing for tests/examples/aut8."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj = parser(
            open(str(Path(TEST_ROOT_DIR, "examples", "aut11.hoa"))).read()
        )  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_hoa(self):
        """Test that the HOA automaton is correct."""
        hoa_header = HOAHeader(
            "v1",
            Acceptance(Atom(0, AtomType.FINITE)),
            nb_states=4,
            start_states=[0, 2, 3],
            acceptance_name="co-Buchi",
            propositions=("a", "b", "c"),
            name="(Fa & G(b&Xc)) | c",
        )

        state_edges_dict = OrderedDict({})
        state_edges_dict[State(0, name="Fa")] = [
            Edge([0], label=TrueLabelExpression(), acc_sig=frozenset({0})),
            Edge([1], label=AtomLabelExpression("0")),
        ]
        state_edges_dict[State(1, name="true")] = [
            Edge([1], label=TrueLabelExpression())
        ]
        state_edges_dict[State(2, name="G(b&Xc)")] = [
            Edge([2, 3], label=AtomLabelExpression("1"))
        ]
        state_edges_dict[State(3, name="c")] = [
            Edge([1], label=AtomLabelExpression("2"))
        ]
        hoa_body = HOABody(state_edges_dict)

        hoa_obj = HOA(hoa_header, hoa_body)
        assert self.hoa_obj == hoa_obj
