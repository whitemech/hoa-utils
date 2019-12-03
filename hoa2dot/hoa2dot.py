#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the command line tool for translating HOA to DOT format."""
import click


@click.command()
@click.argument('infile', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@click.option('-o', '--output', type=click.Path(file_okay=True, dir_okay=False, writable=True),
              help='Path to the output file.')
def main(infile, output):
    """From HOA to DOT format."""


if __name__ == '__main__':
    main()
