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

"""This module contains the configurations for the tests."""
import inspect
import os
from pathlib import Path

TEST_ROOT_DIR = os.path.dirname(inspect.getfile(inspect.currentframe()))  # type: ignore
ROOT_DIR = str(Path(TEST_ROOT_DIR, "..").resolve())  # type: ignore

HOA_FILES = [
    Path(os.path.join(TEST_ROOT_DIR, "examples", "aut1.hoa")),
    Path(os.path.join(TEST_ROOT_DIR, "examples", "aut2.hoa")),
    Path(os.path.join(TEST_ROOT_DIR, "examples", "aut3.hoa")),
    Path(os.path.join(TEST_ROOT_DIR, "examples", "aut3.2.hoa")),
    Path(os.path.join(TEST_ROOT_DIR, "examples", "aut4.hoa")),
    Path(os.path.join(TEST_ROOT_DIR, "examples", "aut5.hoa")),
    Path(os.path.join(TEST_ROOT_DIR, "examples", "aut6.hoa")),
    Path(os.path.join(TEST_ROOT_DIR, "examples", "aut7.hoa")),
    Path(os.path.join(TEST_ROOT_DIR, "examples", "aut8.hoa")),
    Path(os.path.join(TEST_ROOT_DIR, "examples", "aut11.hoa")),
]
