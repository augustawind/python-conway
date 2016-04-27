from conway import ToroidalArray

def test_torroidal_init_recursive():
    t = ToroidalArray([
        [0, 0, 0],
        [0, 1, 1],
        [0, 0, 0]
    ], recursive=True)

    assert isinstance(t, ToroidalArray)
    assert isinstance(t[0], ToroidalArray)
    assert isinstance(t[1], ToroidalArray)
    assert isinstance(t[2], ToroidalArray)

    t = ToroidalArray([[[1]]], recursive=True, depth=1)
    assert isinstance(t, ToroidalArray)
    assert isinstance(t[0], ToroidalArray)
    assert not isinstance(t[0][0], ToroidalArray)

def test_torroidal_getitem():
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

def test_toroidal_setitem():
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

def test_toroidal_delitem():
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
