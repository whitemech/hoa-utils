#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the command line tool for translating HOA to DOT format."""
import click

from hoa2dot.parsers import HOAParser


@click.command()
@click.argument('infile', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@click.option('-o', '--output', type=click.Path(file_okay=True, dir_okay=False, writable=True),
              help='Path to the output file.')
def main(infile, output):
    """From HOA to DOT format."""
    input_string = open(infile).read()
    parser = HOAParser()
    x = parser(input_string)
    print(x)


if __name__ == '__main__':
    main()