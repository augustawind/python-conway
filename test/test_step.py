from conway.grid.toroidal import Grid, Point


def test_rule_1():
    """Any live cell with fewer than 2 live neighbors dies."""
    t = Grid.from_2d_seq([[0, 0, 0], [0, 1, 1], [0, 0, 0]])

    t.nextgen()
    assert len(t) == 0


def test_rule_2():
    """Any live cell with 2 or 3 neighbors lives on."""
    t = Grid.from_2d_seq([[0, 1, 0], [0, 1, 1], [0, 0, 0]])

    t.nextgen()
    assert t[Point(1, 0)] == 1
    assert t[Point(1, 1)] == 1
    assert t[Point(2, 1)] == 1


def test_rule_3():
    """Any live cell with more than 3 live neighbors dies."""
    t = Grid.from_2d_seq(
        [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 1], [0, 0, 0, 0]],
    )

    t.nextgen()
    assert t[Point(2, 1)] == 0
    assert t[Point(2, 2)] == 0


def test_rule_4():
    """Any dead cell with exactly three live neighbors becomees a live cell."""
    t = Grid.from_2d_seq([[0, 0, 0], [0, 0, 1], [0, 1, 1],])

    t.nextgen()
    assert t[Point(1, 1)] == 1
