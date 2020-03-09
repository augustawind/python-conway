import pytest

from conway.grid import Cell
from conway.grid.toroidal import Grid, ToroidalArray

from . import GameRulesTestMixin

T = Cell.ALIVE
F = Cell.DEAD


class TestToroidalArray:
    def test_init_recursive(self):
        t = ToroidalArray([[0, 0, 0], [0, 1, 1], [0, 0, 0]], recursive=True)

        assert isinstance(t, ToroidalArray)
        assert isinstance(t[0], ToroidalArray)
        assert isinstance(t[1], ToroidalArray)
        assert isinstance(t[2], ToroidalArray)

        t = ToroidalArray([[[1]]], recursive=True, depth=1)
        assert isinstance(t, ToroidalArray)
        assert isinstance(t[0], ToroidalArray)
        assert not isinstance(t[0][0], ToroidalArray)

    def test_getitem(self):
        t = ToroidalArray([1, 2, 3])

        assert t[0] == 1
        assert t[1] == 2
        assert t[2] == 3

        assert t[3] == 1
        assert t[4] == 2
        assert t[5] == 3

        assert t[6] == 1
        assert t[7] == 2
        assert t[8] == 3

        assert t[-1] == 3
        assert t[-2] == 2
        assert t[-3] == 1

        assert t[-4] == 3
        assert t[-5] == 2
        assert t[-6] == 1

        assert t[-7] == 3
        assert t[-8] == 2
        assert t[-9] == 1

    def test_setitem(self):
        t = ToroidalArray([1, 2, 3])
        t[1] = 4
        assert t[1] == 4

        t = ToroidalArray([1, 2, 3])
        t[-2] = 4
        assert t[1] == 4

        t = ToroidalArray([1, 2, 3])
        t[-7] = 4
        assert t[2] == 4

        t = ToroidalArray([1, 2, 3])
        t[3] = 4
        assert t[0] == 4

        t = ToroidalArray([1, 2, 3])
        t[6] = 4
        assert t[0] == 4

    def test_delitem(self):
        t = ToroidalArray([1, 2, 3])
        del t[1]
        assert t._list == [1, 3]

        t = ToroidalArray([1, 2, 3])
        del t[-2]
        assert t._list == [1, 3]

        t = ToroidalArray([1, 2, 3])
        del t[-7]
        assert t._list == [1, 2]

        t = ToroidalArray([1, 2, 3])
        del t[3]
        assert t._list == [2, 3]

        t = ToroidalArray([1, 2, 3])
        del t[6]
        assert t._list == [2, 3]


def g2l(grid: Grid) -> list:
    return [list(row) for row in grid.cells]


def tarray(seq=()) -> ToroidalArray:
    return ToroidalArray(seq, recursive=True)


class TestGrid(GameRulesTestMixin):
    GRID_CLS = Grid

    def test_init_with_width_and_height(self):
        grid = Grid(width=3, height=2)
        assert (grid.width, grid.height) == (3, 2)
        assert g2l(grid) == [[F] * 3] * 2

        with pytest.raises(ValueError):
            grid = Grid(width=3)
        with pytest.raises(ValueError):
            grid = Grid(height=3)
        with pytest.raises(ValueError):
            grid = Grid(width=3, height=0)
        with pytest.raises(ValueError):
            grid = Grid(width=0, height=3)
        with pytest.raises(ValueError):
            grid = Grid(width=0, height=0)
        with pytest.raises(ValueError):
            grid = Grid()

    def test_init_with_cells(self):
        grid = Grid(cells=tarray([[1, 0, 0], [0, 1, 1]]))
        assert (grid.width, grid.height) == (3, 2)
        assert g2l(grid) == [[T, F, F], [F, T, T]]

        grid = Grid(cells=tarray([[0, 0, 0], [0, 1, 0], [0, 1, 0]]))
        assert (grid.width, grid.height) == (3, 3)
        assert g2l(grid) == [[F, F, F], [F, T, F], [F, T, F]]

        grid = Grid(
            cells=tarray([[0, 0, 0], [0, 1, 0], [0, 1, 0]]), width=3, height=3
        )
        assert (grid.width, grid.height) == (3, 3)
        assert g2l(grid) == [[F, F, F], [F, T, F], [F, T, F]]

        grid = Grid(cells=tarray([[0, 0, 0], [0, 1, 0], [0, 1, 0]]), width=4)
        assert (grid.width, grid.height) == (4, 3)
        assert g2l(grid) == [[F, F, F, F], [F, T, F, F], [F, T, F, F]]

        grid = Grid(cells=tarray([[0, 0, 0], [0, 1, 0], [0, 1, 0]]), height=4)
        assert (grid.width, grid.height) == (3, 4)
        assert g2l(grid) == [[F, F, F], [F, T, F], [F, T, F], [F, F, F]]

        with pytest.raises(ValueError):
            grid = Grid(
                cells=tarray([[0, 0, 0], [0, 1, 0], [0, 1, 0]]), height=2
            )
        with pytest.raises(ValueError):
            grid = Grid(
                cells=tarray([[0, 0, 0], [0, 1, 0], [0, 1, 0]]), width=2
            )

        with pytest.raises(ValueError):
            grid = Grid(cells=tarray([]))
        with pytest.raises(ValueError):
            grid = Grid(cells=tarray([[]]))
        with pytest.raises(ValueError):
            grid = Grid(cells=tarray([]), width=2)
        with pytest.raises(ValueError):
            grid = Grid(cells=tarray([]), height=2)

        grid = Grid(cells=tarray([[]]), width=2)
        assert (grid.width, grid.height) == (2, 1)
        assert g2l(grid) == [[F, F]]

        grid = Grid(cells=tarray([[], []]), width=2)
        assert (grid.width, grid.height) == (2, 2)
        assert g2l(grid) == [[F, F], [F, F]]
