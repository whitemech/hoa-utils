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
