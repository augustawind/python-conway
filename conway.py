from collections.abc import MutableSequence
from random import randint


class ToroidalArray(MutableSequence):
    '''An array whose indices wrap around indefinitely.'''

    def __init__(self, seq=[]):
        self._list = list(seq)

    def __str__(self):
        return '{}({!s})'.format(self.__class__.__name__, self._list)

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self._list)

    def __len__(self):
        return len(self._list)

    def _wrapped_index(self, index):
        '''Return a regular (wrapped) index given an out of range index.'''
        wrapped = -index % len(self)
        return len(self) - wrapped if wrapped else 0

    def __getitem__(self, index):
        idx = self._wrapped_index(index)
        return self._list[idx]

    def __setitem__(self, index, value):
        idx = self._wrapped_index(index)
        self._list[idx] = value

    def __delitem__(self, index):
        idx = self._wrapped_index(index)
        del self._list[idx]

    def insert(self, index, value):
        return self._list.insert(index, value)

    def __iter__(self):
        return iter(self._list)

    def __add__(self, other):
        right = other._list if isinstance(other, ToroidalArray) else other
        return ToroidalArray(self._list + right)

    def __radd__(self, other):
        left = other._list if isinstance(other, ToroidalArray) else other
        return ToroidalArray(left + self._list)

    def __mul__(self, n):
        return ToroidalArray(self._list * n)

    def __rmul__(self, n):
        return ToroidalArray(self._list * n)


def step(grid):
    '''Apply the rules of the Game of Life to a grid of living and dead cells.

    Arguments:
        grid: ToroidalArray
            A grid of 1's and 0's representing living and dead cells,
            respectively.

    Returns:
        ToroidalArray
            A new grid holding the results of one application of the rules
            of the Game of Life.
    '''
    # List of (x, y) directions: (1, 1), (0, 1), (-1, 1), etc.
    dirs = [(x, y) for x in range(-1, 2) for y in range(-1, 2)
            if x != 0 or y != 0]

    # Results grid.
    grid2 = ToroidalArray()

    for y, row in enumerate(grid):
        grid2.append(ToroidalArray())
        for x, cell in enumerate(row):
            # Count live neighbors of current cell.
            live_neighbors = len([grid[y + j][x + i] for i, j in dirs
                                  if grid[y + j][x + i]])

            # If cell lives has less than 2 or more than 3 live neighbors, it
            # dies.
            if cell and (live_neighbors < 2 or live_neighbors > 3):
                grid2[y].append(0)
            # If cell is dead and has exactly 3 live neighbors, it lives.
            elif live_neighbors == 3:
                grid2[y].append(1)
            # Otherwise, it stays the same.
            else:
                grid2[y].append(grid[y][x])

    return grid2

if __name__ == '__main__':
    width = 10
    height = 10
    grid = ToroidalArray([ToroidalArray([randint(0, 1) for x in range(width)])
                          for y in range(height)])

    done = False
    while not done:
        for row in grid:
            for cell in row:
                print(cell, end='')
            print()
        done = input()
        grid = step(grid)
