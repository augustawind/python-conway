import argparse
import random
import sys
import time
from itertools import cycle

from conway import ToroidalArray, nextgen


def run():
    parser = argparse.ArgumentParser(description="Run Conway's Game of Life "
                                     "cellular automata simulation.")

    parser.add_argument('width', type=int, help='the width of the grid')
    parser.add_argument('height', type=int, help='the height of the grid')

    parser.add_argument('-t', '--turns', type=int, default='-1',
                        help='number of turns to play'
                             ' (default %(default)s, forever)')

    parser.add_argument('-d', '--delay', type=float, default='0.1',
                        help='delay between turns, in seconds'
                             ' (default %(default)s)')

    parser.add_argument('-s', '--separator', type=str, default='\n%\n',
                        help='text separator between output of each turn'
                             ' (default \'\\n%(default)s\\n\')')

    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='output destination (default: stdout)')

    args = parser.parse_args()

    grid1 = ToroidalArray([[random.randint(0, 1) for x in range(args.width)]
                           for y in range(args.height)], recursive=True)
    grid2 = ToroidalArray([[0] * args.width] * args.height, recursive=True)
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
            print('*' if cell else ' ', end='', file=outfile)
        print(file=outfile)


if __name__ == '__main__':
    run()
