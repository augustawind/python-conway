from conway.grid.toroidal import Grid, Point, ToroidalArray


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


class TestRules:
    def test_rule_1(self):
        """Any live cell with fewer than 2 live neighbors dies."""
        t = Grid.from_2d_seq([[0, 0, 0], [0, 1, 1], [0, 0, 0]])

        t.nextgen()
        assert len(t) == 0

    def test_rule_2(self):
        """Any live cell with 2 or 3 neighbors lives on."""
        t = Grid.from_2d_seq([[0, 1, 0], [0, 1, 1], [0, 0, 0]])

        t.nextgen()
        assert t[Point(1, 0)] == 1
        assert t[Point(1, 1)] == 1
        assert t[Point(2, 1)] == 1

    def test_rule_3(self):
        """Any live cell with more than 3 live neighbors dies."""
        t = Grid.from_2d_seq(
            [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 1], [0, 0, 0, 0]],
        )

        t.nextgen()
        assert t[Point(2, 1)] == 0
        assert t[Point(2, 2)] == 0

    def test_rule_4(self):
        """Any dead cell with exactly three live neighbors becomees a live cell."""
        t = Grid.from_2d_seq([[0, 0, 0], [0, 0, 1], [0, 1, 1],])

        t.nextgen()
        assert t[Point(1, 1)] == 1
