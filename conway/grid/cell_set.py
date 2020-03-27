from typing import (
    Any,
    Iterable,
    Iterator,
    MutableSet,
    NamedTuple,
    Sequence,
    Set,
    Tuple,
)

from conway.grid import DIRS, BaseGrid, Point

T = MutableSet[Point]


class Grid(BaseGrid[T]):
    @classmethod
    def from_2d_seq(cls, seq: Sequence[Sequence[Any]], **kwargs) -> "Grid":
        cells = {
            Point(x, y)
            for y, row in enumerate(seq)
            for x, cell in enumerate(row)
            if cell
        }
        return Grid(cells=cells, **kwargs)

    @classmethod
    def from_set(cls, set_: Set[Point], **kwargs) -> "Grid":
        return Grid(cells=set(set_), **kwargs)

    def mk_zeroed_cells(self) -> T:
        return set()

    def calculate_size(self) -> Tuple[int, int]:
        max_x = max_y = 0
        for x, y in self.cells:
            if x + 1 > max_x:
                max_x = x + 1
            if y + 1 > max_y:
                max_y = y + 1
        return max_x, max_y

    @classmethod
    def get_cell(cls, cells: T, point: Point) -> bool:
        return point in cells

    @classmethod
    def set_cell(cls, cells: T, point: Point, value: bool):
        if value:
            cells.add(point)
        else:
            cells.discard(point)

    def enumerate_cells(self) -> Iterator[Tuple[Point, bool]]:
        for y in range(self.height):
            for x in range(self.width):
                point = Point(x, y)
                yield point, self[point]
