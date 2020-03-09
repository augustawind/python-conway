import abc
import random
from collections.abc import Collection
from dataclasses import dataclass, field
from itertools import cycle
from typing import Any, Generic, Iterable, Iterator, NamedTuple, Tuple, TypeVar


class Cell:
    LIVE = True
    DEAD = False


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, rhs: "Point") -> "Point":
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


@dataclass
class BaseGrid(Generic[T], Collection, metaclass=abc.ABCMeta):
    width: int = None
    height: int = None
    cells: T = None
    swap: Iterator[Tuple[T, T]] = field(init=False)

    def __post_init__(self):
        if self.width == 0 or self.height == 0:
            raise ValueError("`width` and `height` must be greater than zero")
        if self.cells is None and not (self.width and self.height):
            raise ValueError(
                "one of (`width` AND `height`) OR `cells` must be set"
            )

        # If `cells` not given, create a zeroed `width` x `height` array.
        if self.cells is None:
            self.cells = self.mk_zeroed_cells()
        # If `cells` is given, ensure it matches the given dimensions.
        else:
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

        swap_cells = self.mk_zeroed_cells()
        self.swap = cycle(((self.cells, swap_cells), (swap_cells, self.cells)))

    @staticmethod
    @abc.abstractmethod
    def from_seq(seq: Iterable[Any], width: int) -> "BaseGrid":
        """Create a Grid from a flat sequence of cells.

        The sequence is split up into rows by the given `width`. Height is
        determined by counting the number of rows after the split.
        """

    @staticmethod
    @abc.abstractmethod
    def from_2d_seq(seq: Iterable[Iterable[Any]]) -> "BaseGrid":
        """Create a Grid from a 2-dimensional sequence of cells.
        
        - It should derive width and height from the sequence's dimensions.
        - Since all Python objects have a truthiness value, it should accept
          any item type and convert each item to a bool if necessary.
        """

    @abc.abstractmethod
    def mk_zeroed_cells(self) -> T:
        """Return a zeroed cells collection (type `T`).

        The returned collection should have the same dimensions as the Grid's
        current cells (width x height).
        """

    @abc.abstractmethod
    def calculate_size(self) -> (int, int):
        """Calculate the width and height of the grid from its `cells`.
        
        Returns the (width, height) pair as a tuple.
        """

    @staticmethod
    @abc.abstractmethod
    def get_cell(cells: T, point: Point) -> bool:
        """Return the cell at the given Point."""

    @staticmethod
    @abc.abstractmethod
    def set_cell(cells: T, point: Point, value: bool):
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

    __contains__ = __getitem__

    def __setitem__(self, point: Point, value: bool):
        return self.set_cell(self.cells, point, value)

    def __iter__(self) -> Iterator[Point]:
        for point, cell in self.enumerate_cells():
            if cell:
                yield Point(x, y)

    def __len__(self) -> int:
        return len(tuple(iter(self)))

    def randomize(self, k=0.5):
        for y in range(self.height):
            for x in range(self.width):
                self[Point(x, y)] = random.random() < k

    def nextgen(self):
        """Update the Grid's cells by applying the Game of Life rules."""
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
