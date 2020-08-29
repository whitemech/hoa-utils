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

"""This module contains the test for the 'hoa.ast.acceptance' module."""

from hoa.ast.acceptance import Acceptance, accepting_sets, Fin, Inf, NotFin, NotInf
from hoa.ast.boolean_expression import PositiveAnd, PositiveOr


def test_accepting_sets():
    """Test the accepting sets."""
    fin0 = Fin(0)
    inf1 = Inf(1)
    not_fin0 = NotFin(0)
    not_inf1 = NotInf(1)

    and_ = fin0 & ~inf1
    or_ = not_fin0 | not_inf1 | and_

    assert isinstance(and_, PositiveAnd)
    assert isinstance(or_, PositiveOr)

    assert accepting_sets(or_) == {0, 1}


def test_acceptance():
    """Test Acceptance instantiation."""
    fin0 = Fin(0)
    Acceptance(fin0, name="fin 0")
