import os
from pathlib import Path

from setuptools import setup


def readme():
    with open(os.path.join(os.path.dirname(__file__), "README.md")) as handle:
        return handle.read()


setup(
    name="conway",
    version="0.0.1",
    author="Dustin Rohde",
    author_email="dustin.rohde@gmail.com",
    license="MIT",
    url="https://github.com/dustinrohde/python-conway",
    description="A Python implementation of Conway's Game of Life.",
    long_description=readme(),
    include_package_data=True,
    packages=["conway", "conway_server"],
    entry_points={"console_scripts": ["conway = conway.__main__:main"]},
)
