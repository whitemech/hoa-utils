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

"""Test the pyhoafparser tool."""
import shutil
import tempfile
from io import StringIO
from pathlib import Path
from unittest import mock
from unittest.mock import MagicMock

import pytest
from click.testing import CliRunner

from hoa.dumpers import dump
from hoa.tools.pyhoafparser import main
from tests.conftest import HOA_FILES
from tests.test_utils import cd


@mock.patch("hoa.dumpers.dumps", return_value="example")
def test_dump(*_mocks):
    """Test the dump method."""
    hoa_object = MagicMock()
    fp = StringIO()
    dump(hoa_object, fp)
    fp.seek(0)
    assert fp.read() == "example"


def test_which_pyhoafparser():
    """Test 'pyhoafparser' is in the PATH."""
    assert shutil.which("pyhoafparser") is not None


@pytest.mark.parametrize(
    "filepath",
    HOA_FILES,
)
def test_pyhoafparser_positive(filepath):
    """Test pyhoafparser, positive case."""
    runner = CliRunner()
    result = runner.invoke(main, [str(filepath.absolute())])
    assert result.exit_code == 0, result.exc_info


@pytest.mark.parametrize(
    "filepath",
    HOA_FILES,
)
def test_pyhoafparser_positive_with_file(filepath):
    """Test pyhoafparser, positive case, with output file."""
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = "output"
        with cd(temp_dir):
            result = runner.invoke(
                main, [str(filepath.absolute()), "--output", output_file]
            )
        assert result.exit_code == 0, result.exc_info
        assert Path(temp_dir, output_file).exists()
