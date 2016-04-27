from collections.abc import MutableSequence, Sequence
from random import randint


class ToroidalArray(MutableSequence):
    '''An array whose indices wrap around indefinitely.

    This basically acts like a Python ``list`` with different behavior for
    ``__getitem__``, ``__setitem__``, and ``__delitem__``. When these methods
    are invoked (through object indexing syntax), indices are "wrapped" so that
    out-of-range indices simply start at the other boundary of the list. For
    negative indicies, this behavior is almost identical to regular lists
    except that a negative index that moves past the beginning of the list will
    continue to wrap around. This behavior is reversed for positive,
    out-of-range indicies.

    Things that work like regular Python ``lists``: membership testing with
    ``in``, iteration, ``sorted`` and ``reversed`` protocols, addition with
    ``+``, repetition with ``*``, ``list`` methods (``insert``, ``append``,
    ``extend``, ``pop``, ``remove``, ``count``).

    Note: Support for slicing is not implemented at this time.

    Args:
        seq (Sequence): A sequence object. Defaults to ``[]``.
        recursive (Optional[bool]): ``True`` if you want to convert any
            sub-sequences in ``seq`` to ``ToroidalArray``s. Defaults to
            ``False``.
        depth (Optional[int]): If ``recursive`` is ``True``, the maximum depth
            at which to recursively convert sequences to ``ToroidalArray``s.
            Defaults to ``-1``, which means no limit is set.
    '''

    def __init__(self, seq=[], recursive=False, depth=-1):
        if recursive:
            for i, item in enumerate(seq):
                if depth and isinstance(item, Sequence):
                    seq[i] = ToroidalArray(item, True, depth - 1)

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
        grid (ToroidalArray): A grid of 1's and 0's representing living and
            dead cells, respectively.

    Returns:
        ToroidalArray: A new grid holding the results of one application of the
            rules of the Game of Life.
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
