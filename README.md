<h1 align="center">
  <b>HOA utils</b>
</h1>

<p align="center">
  <a href="https://pypi.org/project/hoa-utils">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/hoa-utils">
  </a>
  <a href="https://pypi.org/project/hoa-utils">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/hoa-utils" />
  </a>
  <a href="">
    <img alt="PyPI - Status" src="https://img.shields.io/pypi/status/hoa-utils" />
  </a>
  <a href="">
    <img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/hoa-utils" />
  </a>
  <a href="">
    <img alt="PyPI - Wheel" src="https://img.shields.io/pypi/wheel/hoa-utils" />
  </a>
  <a href="https://github.com/whitemech/hoa-utils/blob/master/LICENSE">
    <img alt="GitHub" src="https://img.shields.io/github/license/whitemech/hoa-utils" />
  </a>
</p>
<p align="center">
  <a href="">
    <img alt="test" src="https://github.com/whitemech/hoa-utils/workflows/test/badge.svg">
  </a>
  <a href="">
    <img alt="lint" src="https://github.com/whitemech/hoa-utils/workflows/lint/badge.svg">
  </a>
  <a href="">
    <img alt="docs" src="https://github.com/whitemech/hoa-utils/workflows/docs/badge.svg">
  </a>
  <a href="https://codecov.io/gh/whitemech/hoa-utils">
    <img src="https://codecov.io/gh/whitemech/hoa-utils/branch/master/graph/badge.svg" />
  </a>
</p>
<p align="center">
  <a href="https://img.shields.io/badge/flake8-checked-blueviolet">
    <img alt="" src="https://img.shields.io/badge/flake8-checked-blueviolet">
  </a>
  <a href="https://img.shields.io/badge/mypy-checked-blue">
    <img alt="" src="https://img.shields.io/badge/mypy-checked-blue">
  </a>
  <a href="https://img.shields.io/badge/isort-checked-yellow">
    <img alt="" src="https://img.shields.io/badge/isort-checked-yellow">
  </a>
  <a href="https://img.shields.io/badge/code%20style-black-black">
    <img alt="black" src="https://img.shields.io/badge/code%20style-black-black" />
  </a>
  <a href="https://www.mkdocs.org/">
    <img alt="" src="https://img.shields.io/badge/docs-mkdocs-9cf">
  </a>
</p>

Utilities for the HOA format.

## Install

The best way is to install the package from PyPI:
```
pip install hoa-utils
```

Alternatively, you can install it from source (master branch):
```
pip install git+https://github.com/whitemech/hoa-utils.git
```

## What you'll find

- APIs to create and manipulate HOA objects
- CLI tools to about the HOA format.

The implementation may not be very stable at the moment.

Currently, the only supported CLI tool is:
- `pyhoafparser`: parse and validate a file in HOA format. 


## Development

If you want to contribute, here's how to set up your development environment.

- Install [Poetry](https://python-poetry.org/)
- Clone the repository: `git clone https://github.com/whitemech/hoa-utils.git && cd hoa-utils`
- Install the dependencies: `poetry install`

## Tests

To run tests: `tox`

To run only the code tests: `tox -e py3.7`

To run only the code style checks:
 - `tox -e black-check`
 - `tox -e isort-check`
 - `tox -e flake8`
 
 In `tox.ini` you can find all the test environment supported.

## Docs

To build the docs: `mkdocs build`

To view documentation in a browser: `mkdocs serve`
and then go to [http://localhost:8000](http://localhost:8000)

## Authors

- [Marco Favorito](https://marcofavorito.github.io/)
- [Francesco Fuggitti](https://francescofuggitti.github.io/)

## License

`hoa-utils` is released under the MIT License.

Copyright 2020 WhiteMech
