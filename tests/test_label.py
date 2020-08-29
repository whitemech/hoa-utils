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
