#!/usr/bin/env python3
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


"""This is the command line tool for translating HOA to DOT format."""
from pathlib import Path

import click

from hoa.core import HOA
from hoa.dumpers import dumps
from hoa.parsers import HOAParser


@click.command()
@click.argument(
    "input_file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
)
@click.option(
    "-o",
    "--output",
    type=click.Path(file_okay=True, dir_okay=False, writable=True),
    help="Path to the output file.",
)
def main(input_file, output):
    """Parse and validate a HOA file."""
    input_string = Path(input_file).read_text()
    file = Path(output) if output is not None else None
    parser = HOAParser()
    hoa_obj: HOA = parser(input_string)

    if output is None:
        print(dumps(hoa_obj))
    else:
        with file.open(mode="w") as fout:
            print(dumps(hoa_obj), file=fout)


if __name__ == "__main__":
    main()
