# Test suite for darkf.py
# Copyright (c) 2017 darkf -- licensed under the terms of the MIT license
#
# Uses py.test -- pip install pytest
# then $ py.test

from darkf import *
from darkf import _
from collections import namedtuple

def test_underscore():
    nt = namedtuple('nt', 'x y foo')

    # attribute accessors
    assert _.foo(nt('derp', 1, 42)) == 42

    # item accessors
    assert _[0]([42, 1, 2, 3]) == 42
    assert _['foo']({"foo": 42}) == 42

def test_flatten():
    assert list(flatten([[1, 2], [3, 4], [5, 6]])) == [1, 2, 3, 4, 5, 6]

def test_flatmap():
    assert list(flatmap(lambda x: [x,1], [1, 2, 3])) == [1, 1, 2, 1, 3, 1]

def test_zipwith():
    assert list(zipwith(lambda x, y, z: (x, y, z),
                    [1, 2, 3], [10, 20, 30], [100, 200, 300])) == \
                    [(1, 10, 100), (2, 20, 200), (3, 30, 300)]

def test_group_by():
    assert list(group_by(lambda x,y: x[1] == y[1], [])) == []
    assert list(group_by(lambda x,y: x[1] == y[1], [('x', 1)])) == [[('x', 1)]]
    assert list(group_by(lambda x,y: x[1] == y[1],
               [('f', 10), ('g', 10), ('h', 20), ('i', 20), ('j', 30), ('k', 40)])) == \
               [[('f', 10), ('g', 10)], [('h', 20), ('i', 20)], [('j', 30)], [('k', 40)]]

def test_group():
    assert list(group(["a", "a", "a", "b", "c", "c", "d"])) == \
               [["a", "a", "a"], ["b"], ["c", "c"], ["d"]]

def test_foldl():
    assert foldl1(operator.truediv, [1, 2, 3, 4, 5]) == (((1/2)/3)/4)/5
    assert foldl(operator.truediv, [2, 3, 4, 5], 1) == (((1/2)/3)/4)/5

    assert foldr1(operator.truediv, [1, 2, 3, 4, 5]) == 1/(2/(3/(4/5)))
    # assert foldr(operator.truediv, [2, 3, 4, 5], 1) == 1/(2/(3/(4/5)))

def test_nub():
    assert nub([1, 2, 3, 1, 2, 3, 1, 1]) == [1, 2, 3]

def test_index():
    assert index(1, [1, 2, 3]) == 2 # lists
    assert index(1, range(3)) == 1 # ranges
    assert index(1, (x for x in range(3))) == 1 # iterables

def test_take():
    assert list(take(3, [1, 2, 3, 4, 5, 6])) == [1, 2, 3]

def test_drop():
    assert list(drop(3, [1, 2, 3, 4, 5, 6])) == [4, 5, 6]

def test_length():
    assert length([1, 2, 3]) == 3
    assert length(range(3)) == 3
    assert length(1 for _ in range(3)) == 3

def test_iterate():
    assert list(take(4, iterate(lambda x: x*2, 1))) == [1, 2, 4, 8]
    assert index(3, iterate(lambda x: x*2, 1)) == 2**3