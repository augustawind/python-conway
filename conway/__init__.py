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
    """Run the Game of Life to completion.

    See the ``--help`` output for details.
    """
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
    """Iterate over each tick of the Game.

    Yields a string representation the state of the Game after each tick. The
    first frame yielded is the initial state of the game.

    See the `run` method for argument details.
    """
    yield draw(grid, sep)
    while turns:
        grid.tick()
        yield draw(grid, sep)
        turns -= 1


def render(grid: BaseGrid, sep: str = DEFAULT_SEP, out: IO = DEFAULT_OUTFILE):
    """Print the `grid` to `out` prefixed with the given `sep`."""
    print(draw(grid, sep), file=out)


def draw(grid: BaseGrid, sep: str = DEFAULT_SEP) -> str:
    """Draw the `grid` prefixed with the given `sep`."""
    return f"{sep}\n{grid}"
