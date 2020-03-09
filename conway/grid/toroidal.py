import _collections_abc
from collections.abc import MutableSequence
from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
)

from conway.grid import DIRS, BaseGrid, Cell, Point


class CompositeIterable(Iterable):

    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, C):
        if cls is CompositeIterable:
            return hasattr(C, "__iter__") and not issubclass(C, (str, bytes))
        return NotImplemented


T = TypeVar("T")


class ToroidalArray(MutableSequence, Generic[T]):
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
        self._list: List[T] = list()
        self.recursive = recursive
        self.recursion_depth = depth

        self.extend(seq)

    def __str__(self):
        return "{}({!s})".format(self.__class__.__name__, self._list)

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self._list)

    def _wrapped_index(self, index):
        """Return a regular (wrapped) index given an out of range index."""
        wrapped = -index % len(self)
        if wrapped:
            return len(self) - wrapped
        return 0

    def _process_item(self, item: T) -> Union[T, "ToroidalArray[T]"]:
        """Prepare an item for insertion into the array.

        This should be called by all of the insertion methods (append,
        __setitem__, etc.) on all values coming in to get the correct value.
        """
        if (
            self.recursive
            and self.recursion_depth
            and isinstance(item, CompositeIterable)
            and type(item) is not ToroidalArray
        ):
            return ToroidalArray(
                item, recursive=True, depth=self.recursion_depth - 1
            )
        return item

    def __len__(self):
        return len(self._list)

    def __getitem__(self, index):
        idx = self._wrapped_index(index)
        return self._list[idx]

    def __setitem__(self, index, value):
        idx = self._wrapped_index(index)
        self._list[idx] = self._process_item(value)

    def __delitem__(self, index):
        idx = self._wrapped_index(index)
        del self._list[idx]

    def insert(self, index, value):
        return self._list.insert(index, self._process_item(value))

    def append(self, value):
        self._list.append(self._process_item(value))

    def extend(self, values):
        self._list.extend(self._process_item(val) for val in values)

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


class Grid(BaseGrid[ToroidalArray]):
    def __post_init__(self):
        super().__post_init__()

        # Pad grid with dead rows to reach `self.height`.
        padding = max(0, self.height - len(self.cells))
        self.cells.extend(
            [Cell.DEAD for _ in range(self.width)] for _ in range(padding)
        )

        # Pad short rows with dead cells to reach `self.width`.
        for row in self.cells:
            padding = max(0, self.width - len(row))
            row.extend(Cell.DEAD for _ in range(padding))

    @classmethod
    def from_2d_seq(cls, seq: Sequence[Sequence[Any]], **kwargs) -> "Grid":
        cells = [[bool(cell) for cell in row] for row in seq]
        return Grid(
            cells=ToroidalArray(cells, recursive=True, depth=1), **kwargs
        )

    @classmethod
    def from_set(cls, set_: Set[Point], **kwargs) -> "Grid":
        width = kwargs.get("width") or max(x for x, _ in set_)
        height = kwargs.get("height") or max(y for _, y in set_)
        return cls.from_2d_seq(
            [
                [Point(x, y) in set_ for x in range(width)]
                for y in range(height)
            ],
            width=width,
            height=height,
        )

    def mk_zeroed_cells(self) -> ToroidalArray:
        return ToroidalArray(
            [
                [Cell.DEAD for _ in range(self.width)]
                for _ in range(self.height)
            ],
            recursive=True,
            depth=1,
        )

    def calculate_size(self) -> Tuple[int, int]:
        width = max(len(row) for row in self.cells)
        height = len(self.cells)
        return width, height

    @classmethod
    def get_cell(cls, cells: ToroidalArray, point: Point) -> bool:
        return cells[point.y][point.x]

    @classmethod
    def set_cell(cls, cells: ToroidalArray, point: Point, value: bool):
        cells[point.y][point.x] = value

    def enumerate_cells(self) -> Iterator[Tuple[Point, bool]]:
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                yield Point(x, y), cell

    def count_live_neighbors(self, point: Point) -> int:
        return sum(self[point + delta] for delta in DIRS)
