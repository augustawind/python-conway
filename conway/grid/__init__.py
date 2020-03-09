import abc
import copy
import itertools
import random
from collections.abc import Collection
from dataclasses import dataclass, field
from itertools import cycle
from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    NamedTuple,
    Sequence,
    Set,
    Tuple,
    TypeVar,
)


class Cell:
    ALIVE = True
    DEAD = False


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, rhs: "Point") -> "Point":  # type: ignore
        return Point(self.x + rhs.x, self.y + rhs.y)


DIRS = {
    Point(x, y)
    for x, y in (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    )
}


T = TypeVar("T")


@dataclass  # type: ignore
class BaseGrid(Generic[T], Collection, metaclass=abc.ABCMeta):
    width: int = None  # type: ignore
    height: int = None  # type: ignore
    cells: T = None  # type: ignore
    swap: Iterator[Tuple[T, T]] = field(init=False)

    def __post_init__(self):
        if self.cells is None and not (self.width and self.height):
            raise ValueError(
                "one of (`width` AND `height`) OR `cells` must be set"
            )

        # If `cells` not given, create a zeroed `width` x `height` array.
        if self.cells is None:
            self.cells = self.mk_zeroed_cells()
        # If `cells` is given, ensure it matches the given dimensions.
        else:
            # Prevent mutation of external object passed in `cells`.
            self.cells = copy.copy(self.cells)
            width, height = self.calculate_size()

            if self.height is None:
                self.height = height
            elif self.height < height:
                raise ValueError(
                    "given `height` does not match actual height of `cells`"
                )

            if self.width is None:
                self.width = width
            elif self.width < width:
                raise ValueError(
                    "given `width` does not match actual width of `cells`"
                )

        if self.width == 0 or self.height == 0:
            raise ValueError("`width` and `height` must be greater than zero")

        swap_cells = self.mk_zeroed_cells()
        self.swap = cycle(((self.cells, swap_cells), (swap_cells, self.cells)))

    def __str__(self):
        return "\n".join(
            "".join([cell and "*" or "." for _, cell in row])
            for row in chunks(tuple(self.enumerate_cells()), self.width)
        )

    @classmethod
    @abc.abstractmethod
    def from_2d_seq(cls, seq: Sequence[Sequence[Any]], **kwargs) -> "BaseGrid":
        """Create a Grid from a 2-dimensional sequence of cells.

        - It should derive width and height from the sequence's dimensions.
        - Since all Python objects have a truthiness value, it should accept
          any item type and convert each item to a bool if necessary.
        """

    @classmethod
    def from_seq(cls, seq: Sequence[Any], width: int, **kwargs) -> "BaseGrid":
        """Create a Grid from a flat sequence of cells.

        The sequence is split up into rows by the given `width`.
        """
        cells = chunks(seq, width)
        return cls.from_2d_seq(tuple(cells), width=width, **kwargs)

    @classmethod
    @abc.abstractmethod
    def from_set(cls, set_: Set[Point], **kwargs) -> "BaseGrid":
        return NotImplemented

    @classmethod
    def from_str(cls, s: str, char_alive: str = "*", **kwargs) -> "BaseGrid":
        """Parse a Grid from a string.

        Each line in the `s` represents a row in the grid, and every char in
        that line represents a cell in that row. If it's `char_alive` it's
        read as a living cell; any other character is read as a dead cell.

        Any whitespace at the beginning or end of each line is ignored.
        """
        cells = [
            [ch == char_alive for ch in line.strip()]
            for line in s.strip().splitlines()
        ]
        return cls.from_2d_seq(cells, **kwargs)

    @abc.abstractmethod
    def mk_zeroed_cells(self) -> T:
        """Return a zeroed cells collection (type `T`).

        The returned collection should have the same dimensions as the
        Grid's current cells (width x height).
        """

    @abc.abstractmethod
    def calculate_size(self) -> Tuple[int, int]:
        """Calculate the width and height of the grid from its `cells`.

        Returns the (width, height) pair as a tuple.
        """

    @classmethod
    @abc.abstractmethod
    def get_cell(cls, cells: T, point: Point) -> bool:
        """Return the cell at the given Point."""

    @classmethod
    @abc.abstractmethod
    def set_cell(cls, cells: T, point: Point, value: bool):
        """Set the cell at the given Point to the given value."""

    @abc.abstractmethod
    def enumerate_cells(self) -> Iterator[Tuple[Point, bool]]:
        """Return an iterator over every cell in the Grid.

        It should yield (point, cell) pairs from right to left, one row at a
        time, starting with the top-left of the grid ((0, 0)).

        For example, in a 3x3 grid, the output should look like this:

            (((0, 0), x), ((1, 0), x), ((2, 0), x),
             ((0, 1), x), ((1, 1), x), ((2, 1), x),
             ((0, 2), x), ((1, 2), x), ((2, 2), x))

        where `x` is the value of the cell at each Point.
        """

    @abc.abstractmethod
    def count_live_neighbors(self, point: Point) -> int:
        """Return the number of live neighbors adjacent to the given Point."""

    def __getitem__(self, point: Point) -> bool:
        return self.get_cell(self.cells, point)

    def __contains__(self, item: object) -> bool:
        if not isinstance(item, Point):
            raise TypeError(f"expected a Point, got {type(item)}")
        return self.__getitem__(item)

    def __setitem__(self, point: Point, value: bool):
        return self.set_cell(self.cells, point, value)

    def __iter__(self) -> Iterator[Point]:
        return (point for point, cell in self.enumerate_cells() if cell)

    def __len__(self) -> int:
        return len(tuple(iter(self)))

    def randomize(self, k=0.5):
        for y in range(self.height):
            for x in range(self.width):
                self[Point(x, y)] = random.random() < k

    def tick(self):
        """Advance the Grid forward by one step.
        
        Generates a new generation of cells by applying the Game of Life
        rules to each cell simultaneously, then updates the Grid with the
        result.
        """
        cells, next_cells = next(self.swap)

        for point, cell in self.enumerate_cells():
            # Count live neighbors of current cell.
            live_neighbors = self.count_live_neighbors(point)

            # If cell has less than 2 or more than 3 live neighbors, it's dead.
            if live_neighbors < 2 or live_neighbors > 3:
                self.set_cell(next_cells, point, False)
            # If cell has exactly 3 live neighbors, it's alive.
            elif live_neighbors == 3:
                self.set_cell(next_cells, point, True)
            # Otherwise, it stays the same.
            else:
                self.set_cell(next_cells, point, self[point])

        self.cells = next_cells


def chunks(seq: Sequence, chunk_size: int) -> Iterator[Sequence]:
    start, end = 0, chunk_size
    while start < len(seq):
        yield seq[start:end]
        start, end = end, end + chunk_size
