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

"""Test the printer module."""
from hoa2dot.ast.acceptance import Fin, NotInf
from hoa2dot.ast.label import LabelAlias, LabelAtom
from hoa2dot.printers import acceptance_condition_to_string, label_expression_to_string


def test_printer_acceptance():
    """Test the printer for acceptance conditions."""
    fin0 = Fin(0)
    notinf0 = NotInf(1)
    and_ = fin0 & notinf0
    or_ = fin0 | and_

    expected = "(Fin(0) | (Fin(0) & Inf(!1)))"
    actual = acceptance_condition_to_string(or_)
    assert expected == actual


def test_printer_label():
    """Test the printer for label expressions."""
    a = LabelAtom("a")
    b = LabelAtom("b")
    c = LabelAtom("c")
    d = LabelAlias("d", a & b)

    or_ = c | d
    not_ = ~or_

    expected = "(!(c | @d))"
    actual = label_expression_to_string(not_)
    assert expected == actual
