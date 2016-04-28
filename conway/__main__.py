import argparse
import random
import sys
import time

from conway import ToroidalArray, step


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

    grid = ToroidalArray([[random.randint(0, 1) for x in range(args.width)]
                          for y in range(args.height)], recursive=True)

    show_grid(grid, args.outfile)

    while args.turns:
        print(args.separator, file=args.outfile)

        show_grid(grid, args.outfile)

        time.sleep(args.delay)
        grid = step(grid)
        args.turns -= 1


def show_grid(grid, outfile):
    for row in grid:
        for cell in row:
            print('*' if cell else ' ', end='', file=outfile)
        print(file=outfile)


if __name__ == '__main__':
    run()
