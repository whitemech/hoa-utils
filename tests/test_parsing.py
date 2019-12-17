# -*- coding: utf-8 -*-
"""Test the parsing module."""
from pathlib import Path

from hoa2dot.core import HOA
from hoa2dot.parsers import HOAParser
from .conftest import CUR_PATH


class TestParsingAut1:
    """Test parsing for tests/examples/aut1."""

    @classmethod
    def setup_class(cls):
        """Set the test up."""
        parser = HOAParser()
        cls.hoa_obj = parser(open(str(Path(CUR_PATH, "examples", "aut1.hoa"))).read())  # type: HOA
        cls.hoa_header = cls.hoa_obj.header
        cls.hoa_body = cls.hoa_obj.body

    def test_format_version(self):
        """Test that the format version is correct."""
        assert self.hoa_header.format_version == "v1"

    # TODO many other tests...
