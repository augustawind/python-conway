import argparse
import random
import sys
import time
from itertools import cycle
from typing import IO

import conway
from conway.grid.cell_set import Grid


def main():
    parser = argparse.ArgumentParser(
        prog="conway",
        description="Conway's Game of Life, a cellular automata simulation.",
    )
    parser.add_argument("width", type=int, help="the width of the grid")
    parser.add_argument("height", type=int, help="the height of the grid")
    parser.add_argument(
        "-t",
        "--turns",
        type=int,
        default=conway.DEFAULT_TURNS,
        help="number of turns to play (default: forever)",
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default=conway.DEFAULT_DELAY,
        help="delay between turns, in seconds (default: %(default)s)",
    )
    parser.add_argument(
        "-s",
        "--separator",
        type=str,
        default=conway.DEFAULT_SEP,
        help="char(s) used to separate each turn's output"
        " (default: %(default)s)",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        type=argparse.FileType("w"),
        default=conway.DEFAULT_OUTFILE,
        help="output destination (default: %(default)s)",
    )
    args = parser.parse_args()

    grid = Grid.from_2d_seq(
        [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )
    # grid = Grid(args.width, args.height)
    # grid.randomize()

    # Expand separator to a full line.
    args.separator *= grid.width // len(args.separator)

    # Run it!
    conway.run(
        grid,
        delay=args.delay,
        sep=args.separator,
        turns=args.turns,
        out=args.outfile,
    )


if __name__ == "__main__":
    main()
