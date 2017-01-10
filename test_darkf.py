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