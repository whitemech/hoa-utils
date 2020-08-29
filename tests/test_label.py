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

"""This module contains the test for the 'hoa.ast.label' module."""

from hoa.ast.boolean_expression import And, Not, Or
from hoa.ast.label import LabelAlias, LabelAtom, propositions
from hoa.types import alias


def test_propositions():
    """Test the accepting sets."""
    a = LabelAtom(0)
    b = LabelAtom(1)
    a_and_b = a & b
    c = LabelAtom(2)
    d = LabelAlias(alias("@d"), a & b)

    or_ = c | d
    not_ = ~or_

    assert isinstance(a_and_b, And)
    assert isinstance(or_, Or)
    assert isinstance(not_, Not)

    assert propositions(not_) == {0, 1, 2}