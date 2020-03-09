from conway.grid import BaseGrid, Point


class GridTests:
    GRID_CLS: BaseGrid

    def test_rule_1(self):
        """Any live cell with fewer than 2 live neighbors dies."""
        grid = self.GRID_CLS.from_2d_seq([[0, 0, 0], [0, 1, 1], [0, 0, 0]])

        grid.nextgen()
        assert len(grid) == 0

    def test_rule_2(self):
        """Any live cell with 2 or 3 neighbors lives on."""
        grid = self.GRID_CLS.from_2d_seq([[0, 1, 0], [0, 1, 1], [0, 0, 0]])

        grid.nextgen()
        assert grid[Point(1, 0)] == 1
        assert grid[Point(1, 1)] == 1
        assert grid[Point(2, 1)] == 1

    def test_rule_3(self):
        """Any live cell with more than 3 live neighbors dies."""
        grid = self.GRID_CLS.from_2d_seq(
            [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 1], [0, 0, 0, 0]]
        )

        grid.nextgen()
        assert grid[Point(2, 1)] == 0
        assert grid[Point(2, 2)] == 0

    def test_rule_4(self):
        """Any dead cell with exactly three live neighbors becomees a live cell."""
        grid = self.GRID_CLS.from_2d_seq([[0, 0, 0], [0, 0, 1], [0, 1, 1]])

        grid.nextgen()
        assert grid[Point(1, 1)] == 1
