import pytest

from conway.grid import Cell, Point
from conway.grid.cell_set import Grid

P = Point
T = Cell.ALIVE
F = Cell.DEAD


class TestGrid:
    def test_init_with_width_and_height(self):
        grid = Grid(width=3, height=2)
        assert (grid.width, grid.height) == (3, 2)
        assert grid.cells == set()

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
        cells = {P(0, 0), P(1, 1), P(2, 1)}
        grid = Grid(cells=cells)
        assert (grid.width, grid.height) == (3, 2)
        assert grid.cells == cells

        cells = {P(1, 1), P(1, 2)}

        grid = Grid(cells=cells.copy())
        assert (grid.width, grid.height) == (2, 3)
        assert grid.cells == cells

        grid = Grid(cells=cells.copy(), width=2, height=3)
        assert (grid.width, grid.height) == (2, 3)
        assert grid.cells == cells

        grid = Grid(cells=cells.copy(), width=4)
        assert (grid.width, grid.height) == (4, 3)
        assert grid.cells == cells

        grid = Grid(cells=cells.copy(), height=4)
        assert (grid.width, grid.height) == (2, 4)
        assert grid.cells == cells

        with pytest.raises(ValueError):
            grid = Grid(cells=cells.copy(), height=2)
        with pytest.raises(ValueError):
            grid = Grid(cells=cells.copy(), width=1)

        with pytest.raises(ValueError):
            grid = Grid(cells=set())
        with pytest.raises(ValueError):
            grid = Grid(cells=set(), width=2)
        with pytest.raises(ValueError):
            grid = Grid(cells=set(), height=2)
