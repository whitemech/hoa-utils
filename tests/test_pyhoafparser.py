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
