import argparse
import sys
import time
from typing import IO, Iterator

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
        grid.tick()
        render(grid, sep, out)
        time.sleep(delay)
        turns -= 1


def run_iter(
    grid: BaseGrid, sep: str = DEFAULT_SEP, turns: int = DEFAULT_TURNS
) -> Iterator[str]:
    yield draw(grid, sep)
    while turns:
        grid.tick()
        yield draw(grid, sep)
        turns -= 1


def render(grid: BaseGrid, sep: str = DEFAULT_SEP, out: IO = DEFAULT_OUTFILE):
    print(draw(grid, sep), file=out)


def draw(grid: BaseGrid, sep: str = DEFAULT_SEP) -> str:
    return f"{sep}\n{grid}"
