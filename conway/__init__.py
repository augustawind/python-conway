import argparse
import time
from typing import IO

from conway.grid import BaseGrid


def play(grid: BaseGrid, delay: float, sep: str, turns: int, outfile: IO):
    render(grid, sep, outfile)
    time.sleep(delay)

    while turns:
        grid.nextgen()
        render(grid, sep, outfile)
        time.sleep(delay)
        turns -= 1


def play_iter(grid: BaseGrid, sep: str, turns: int):
    while turns:
        yield tick(grid)
        turns -= 1


def tick(grid: BaseGrid):
    grid.nextgen()
    return str(grid)


def render(grid: BaseGrid, sep: str, outfile: IO):
    print(f"{sep}\n{grid}")
