import argparse
import time
from typing import IO

from conway.grid import BaseGrid


def run(grid: BaseGrid, delay: float, sep: str, turns: int, outfile: IO):
    render(grid, sep, outfile)
    time.sleep(delay)

    while turns:
        grid.nextgen()
        render(grid, sep, outfile)
        time.sleep(delay)
        turns -= 1


def run_iter(grid: BaseGrid, sep: str, turns: int):
    yield draw(grid, sep)

    while turns:
        grid.nextgen()
        yield draw(grid, sep)
        turns -= 1


def render(grid: BaseGrid, sep: str, outfile: IO):
    print(draw(grid, sep), file=outfile)


def draw(grid: BaseGrid, sep: str) -> str:
    return f"{sep}\n{grid}"
