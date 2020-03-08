from collections.abc import Iterable, MutableSequence


class ToroidalArray(MutableSequence):
    """An array whose indices wrap around indefinitely.

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
        seq: An iterable whose items will populate the TorroidalArray.
        recursive: Whether to convert any nested iterables in ``seq`` to
            ToroidalArrays. This will not convert ``str`` or ``bytes`` objects.
        depth: Maximum depth to traverse if ``recursive=True``. Use a
            negative number for no limit (the default).
    """

    def __init__(
        self, seq: Iterable = (), recursive: bool = False, depth: int = -1
    ):
        self._list = list(seq)
        if recursive and depth:
            for i, item in enumerate(self._list):
                if not isinstance(item, (str, bytes)) and isinstance(
                    item, Iterable
                ):
                    self._list[i] = ToroidalArray(item, True, depth - 1)

    def __str__(self):
        return "{}({!s})".format(self.__class__.__name__, self._list)

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self._list)

    def __len__(self):
        return len(self._list)

    def _wrapped_index(self, index):
        """Return a regular (wrapped) index given an out of range index."""
        wrapped = -index % len(self)
        if wrapped:
            return len(self) - wrapped
        return 0

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


# List of 8 (x, y) directions.
dirs = {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}


def nextgen(grid1: ToroidalArray, grid2: ToroidalArray):
    """Apply the rules of the Game of Life to a grid of living and dead cells.

    Arguments:
        grid1 (ToroidalArray): A grid of 1's and 0's representing living and
            dead cells, respectively.
        grid2 (ToroidalArray): Results grid. Contents don't matter, as they
            will all be replaced, but must be the same size as ``grid1``.
            This grid will be populated with the results of one application
            of the rules of the Game of Life.
    """
    for y, row in enumerate(grid1):
        for x in range(len(row)):
            # Count live neighbors of current cell.
            live_neighbors = sum([grid1[y + j][x + i] for i, j in dirs])

            # If cell has less than 2 or more than 3 live neighbors, it's dead.
            if live_neighbors < 2 or live_neighbors > 3:
                grid2[y][x] = 0
            # If cell has exactly 3 live neighbors, it's alive.
            elif live_neighbors == 3:
                grid2[y][x] = 1
            # Otherwise, it stays the same.
            else:
                grid2[y][x] = grid1[y][x]

    return grid2
