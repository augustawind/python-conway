from typing import NamedTuple


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
