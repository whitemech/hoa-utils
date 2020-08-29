# -*- coding: utf-8 -*-
# This file is part of hoa-utils.
#
# hoa-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# hoa-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with hoa-utils.  If not, see <https://www.gnu.org/licenses/>.
#

"""Test the printer module."""
from hoa.ast.acceptance import Fin, NotInf
from hoa.ast.label import LabelAlias, LabelAtom
from hoa.printers import acceptance_condition_to_string, label_expression_to_string
from hoa.types import alias


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
    a = LabelAtom(0)
    b = LabelAtom(1)
    c = LabelAtom(2)
    d = LabelAlias(alias("@d"), a & b)

    or_ = c | d
    not_ = ~or_

    expected = "(!(2 | @d))"
    actual = label_expression_to_string(not_)
    assert actual == expected
