import argparse
import sys
import time
from typing import IO

from conway.grid import BaseGrid

DEFAULT_TURNS = -1
DEFAULT_DELAY = 0.35
DEFAULT_SEP = "%"
DEFAULT_OUTFILE = sys.stdout


def run(
    grid: BaseGrid,
    turns: int = DEFAULT_TURNS,
    delay: float = DEFAULT_DELAY,
    sep: str = DEFAULT_SEP,
    out: IO = DEFAULT_OUTFILE,
):
    render(grid, sep, out)
    time.sleep(delay)

    while turns:
        grid.nextgen()
        render(grid, sep, out)
        time.sleep(delay)
        turns -= 1


def run_iter(grid: BaseGrid, sep: str, turns: int):
    yield draw(grid, sep)

    while turns:
        grid.nextgen()
        yield draw(grid, sep)
        turns -= 1


def render(grid: BaseGrid, sep: str, out: IO):
    print(draw(grid, sep), file=out)


def draw(grid: BaseGrid, sep: str) -> str:
    return f"{sep}\n{grid}"
