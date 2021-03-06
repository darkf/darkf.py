# Test suite for darkf.py
# Copyright (c) 2017 darkf -- licensed under the terms of the MIT license
#
# Uses py.test -- pip install pytest
# then $ py.test

from darkf import *
from darkf import _
from collections import namedtuple
import math
import pytest

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

def test_foldr():
    assert foldr1(operator.truediv, [1, 2, 3, 4, 5]) == 1/(2/(3/(4/5)))
    # assert foldr(operator.truediv, [2, 3, 4, 5], 1) == 1/(2/(3/(4/5)))

def test_scanl():
    assert list(scanl1(operator.add, [1, 2, 3])) == [1, 3, 6]
    assert list(scanl1(operator.mul, [1, 2, 3])) == [1, 2, 6]

def test_nub():
    assert nub([1, 2, 3, 1, 2, 3, 1, 1]) == [1, 2, 3]

def test_index():
    assert index(1, [1, 2, 3]) == 2 # lists
    assert index(1, range(3)) == 1 # ranges
    assert index(1, (x for x in range(3))) == 1 # iterables

    with pytest.raises(IndexError):
        index(1, [])
        index(1, range(1))

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

def test_find():
    assert find(lambda x: x > 2, [1, 2, 3, 4, 5]) == 3

def test_find_index():
    assert find_index(lambda x: x > 2, [1, 2, 3, 4, 5]) == 2

def test_partition():
    assert partition(lambda x: x <= 3, [1, 2, 3, 4, 5, 6]) == ([1, 2, 3], [4, 5, 6])
    assert partition(lambda x: x <= 3, []) == ([], [])
    assert partition(lambda x: x <= 3, [1]) == ([1], [])

def test_product():
    assert product(range(1, 10+1)) == math.factorial(10)

def test_transpose():
    assert transpose([ [1, 2, 3],
                       [4, 5, 6] ]) == [[1, 4],
                                        [2, 5],
                                        [3, 6]]

def test_cons():
    assert cons(1, [2, 3]) == [1, 2, 3]

def test_mapfst_mapsnd():
    assert mapfst(lambda x: x*2, (5, 10)) == (10, 10)
    assert mapsnd(lambda x: x*2, (5, 10)) == (5, 20)

def test_uncons():
    assert mapsnd(list, uncons([1, 2, 3])) == (1, [2, 3])

def test_head_tail():
    assert head([1, 2, 3]) == 1
    assert list(tail([1, 2, 3])) == [2, 3]

def test_lines_unlines():
    assert lines("a\nb\ncd") == ["a", "b", "cd"]
    assert unlines(["a", "b", "cd"]) == "a\nb\ncd"

def test_words_unwords():
    assert words("a b cd") == ["a", "b", "cd"]
    assert unwords(["a", "b", "cd"]) == "a b cd"

def test_bimap():
    bimap = BiMap(a=1, b=2)

    # forward mapping
    assert bimap["a"] == 1
    assert bimap["b"] == 2

    # backward mapping
    assert bimap[1] == "a"
    assert bimap[2] == "b"

    # length
    assert len(bimap) == 2*2

    # mutation
    bimap["a"] = 42
    assert bimap["a"] == 42
    assert bimap[42] == "a"

    # assert length didn't change
    assert len(bimap) == 2*2

    # invalid keys
    with pytest.raises(KeyError):
        bimap["c"]
        bimap[3]

    # get
    assert bimap.get("c") == None
    assert bimap.get("c", 42) == 42

    # keys
    assert set(bimap.keys()) == {"a", "b", 42, 2}

    # values
    assert set(bimap.values()) == {"a", "b", 42, 2}
