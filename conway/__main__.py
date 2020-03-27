import argparse
import random
import sys
import time
from itertools import cycle
from pathlib import Path
from typing import IO

import conway
from conway.grid.cell_set import Grid

SAMPLE_DIR = Path(__file__).parent.parent.absolute() / "sample_patterns"
SAMPLE_CHOICES = ("beacon", "blinker", "glider", "toad")


def main():
    parser = argparse.ArgumentParser(
        prog="conway",
        description="Conway's Game of Life, a cellular automata simulation.",
        add_help=False,
    )
    parser.add_argument(
        "--help", action="help", help="show this help message and exit"
    )

    source_group = parser.add_mutually_exclusive_group(required=True)
    arg_random = source_group.add_argument(
        "--random",
        type=float,
        nargs="?",
        const=0.5,
        metavar="K",
        help=(
            "randomly generate the initial grid. if given, %(metavar)s must"
            " be a number in the range [0, 1) and sets the probability that a"
            " cell will be living (default: %(const)s)"
        ),
    )
    arg_sample = source_group.add_argument(
        "--sample",
        type=str,
        choices=SAMPLE_CHOICES,
        metavar="PATTERN",
        help="set the initial grid to a predefined sample pattern",
    )
    arg_file = source_group.add_argument(
        "--file",
        type=argparse.FileType("r"),
        default=sys.stdin,
        metavar="FILE",
        help="set the initial grid to a custom pattern file",
    )

    parser.add_argument(
        "-c",
        "--char-alive",
        default="*",
        metavar="CHAR",
        help=(
            "char that represents a living cell when used with the"
            " {s} or {f} options".format(
                s=fmt_arg(arg_sample), f=fmt_arg(arg_file)
            )
        ),
    )

    arg_width = parser.add_argument(
        "-w", "--width", type=int, help="the width of the grid"
    )
    arg_height = parser.add_argument(
        "-h", "--height", type=int, help="the height of the grid"
    )
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
        help=(
            "char(s) used to separate each turn's output"
            " (default: %(default)s)"
        ),
    )
    parser.add_argument(
        "-o",
        "--outfile",
        type=argparse.FileType("w"),
        default=conway.DEFAULT_OUTFILE,
        help="output destination (default: %(default)s)",
    )
    args = parser.parse_args()

    # Randomly generate the grid.
    if args.random is not None:
        if not (args.width and args.height):
            parser.error(
                "{w} and {h} are required to use {r}".format(
                    w=fmt_arg(arg_width),
                    h=fmt_arg(arg_height),
                    r=fmt_arg(arg_random),
                )
            )
        grid = Grid(args.width, args.height)
        grid.randomize(k=args.random)

    # Load a sample pattern.
    elif args.sample:
        sample_path = SAMPLE_DIR / args.sample
        with open(sample_path) as fd:
            pattern = fd.read()
        grid = Grid.from_str(pattern, char_alive=args.char_alive)

    # Load a pattern from a file.
    elif args.file:
        pattern = args.file.read()
        grid = Grid.from_str(pattern, char_alive=args.char_alive)

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


def fmt_arg(arg: argparse.Action):
    return "/".join(arg.option_strings)


if __name__ == "__main__":
    main()
