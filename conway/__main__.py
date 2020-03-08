import argparse
import random
import sys
import time
from itertools import cycle

from conway.torroidal import Grid, nextgen


def run():
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
        default="-1",
        help="number of turns to play (default: forever)",
    )

    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default="0.1",
        help="delay between turns, in seconds (default: %(default)s)",
    )

    parser.add_argument(
        "-s",
        "--separator",
        type=str,
        default="+N---+N",
        help="text separator between output of each turn; the character"
        " sequence `+N` denotes a newline (default: %(default)s')",
    )
    parser.add_argument(
        "-p", "--padding", type=int, default=2,
    )

    parser.add_argument(
        "-o",
        "--outfile",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="output destination (default: %(default)s)",
    )

    args = parser.parse_args()

    args.separator = args.separator.replace("+N", "\n")

    grid1 = Grid(args.width, args.height)
    grid1.randomize()
    grid2 = Grid(args.width, args.height)
    gridswap = cycle(((grid1, grid2), (grid2, grid1)))

    while args.turns:
        time.sleep(args.delay)
        print(args.separator, file=args.outfile)

        grid1, grid2 = next(gridswap)
        show_grid(grid1, args.outfile)
        nextgen(grid1, grid2)

        args.turns -= 1


def show_grid(grid, outfile):
    for row in grid:
        for cell in row:
            print("*" if cell else " ", end="", file=outfile)
        print(file=outfile)


if __name__ == "__main__":
    run()
