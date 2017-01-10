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