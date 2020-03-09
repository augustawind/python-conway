from typing import Any, Iterable, Iterator, MutableSet, NamedTuple, Tuple

from conway.grid import DIRS, BaseGrid, Point


class Grid(BaseGrid[MutableSet[Point]]):
    @classmethod
    def from_2d_seq(cls, seq: Iterable[Iterable[Any]]) -> "Grid":
        cells = {
            Point(x, y)
            for y, row in enumerate(seq)
            for x, cell in enumerate(row)
            if cell
        }
        return Grid(cells=cells)

    def mk_zeroed_cells(self) -> MutableSet[Point]:
        return set()

    def calculate_size(self) -> (int, int):
        max_x = max_y = 0
        for x, y in self.cells:
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
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
