from typing import (
    Any,
    Iterable,
    Iterator,
    MutableSet,
    NamedTuple,
    Sequence,
    Tuple,
)

from conway.grid import DIRS, BaseGrid, Point


class Grid(BaseGrid[MutableSet[Point]]):
    @classmethod
    def from_2d_seq(cls, seq: Sequence[Sequence[Any]]) -> "Grid":
        width = max(len(row) for row in seq)
        height = len(seq)
        cells = {
            Point(x, y)
            for y, row in enumerate(seq)
            for x, cell in enumerate(row)
            if cell
        }
        return Grid(width, height, cells=cells)

    def mk_zeroed_cells(self) -> MutableSet[Point]:
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
    def get_cell(cls, cells: MutableSet[Point], point: Point) -> bool:
        return point in cells

    @classmethod
    def set_cell(cls, cells: MutableSet[Point], point: Point, value: bool):
        if value:
            cells.add(point)
        else:
            cells.discard(point)

    def enumerate_cells(self) -> Iterator[Tuple[Point, bool]]:
        for y in range(self.height):
            for x in range(self.width):
                point = Point(x, y)
                yield point, self[point]

    def count_live_neighbors(self, point: Point) -> int:
        return sum(point + delta in self.cells for delta in DIRS)
