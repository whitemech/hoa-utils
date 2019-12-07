# -*- coding: utf-8 -*-
"""Test the hoa2dot tool."""

from pathlib import Path

from click.testing import CliRunner

from hoa2dot import hoa2dot
from .conftest import CUR_PATH


def test_aut1():
    """Test tests/examples/aut1."""
    cli = CliRunner()
    result = cli.invoke(hoa2dot.main, args=[str(Path(CUR_PATH, "examples", "aut1.hoa"))])
    assert result.exit_code == 0
    # print(result.output)
