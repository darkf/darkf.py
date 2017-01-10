# darkf.py -- a supplemental standard library by darkf
# Copyright (c) 2017 darkf -- licensed under the terms of the MIT license
#
# NOTE: _ will have to be imported explicitly, if desired.

import itertools, functools, operator

class UnderscoreProxy:
    """A proxy object that returns accessors for attributes and
       items looked up on it.

       Example: _.foo is the same as lambda x: x.foo
                _["foo"] is the same as lambda x: x["foo"]

       It is useful for producing higher-order functions with nicer
       syntax than operator.itemgetter.
    """

    def __getattr__(self, attr):
        return lambda x: getattr(x, attr)
    
    def __getitem__(self, item):
        return lambda x: x[item]

_ = UnderscoreProxy()

def flatten(xs):
    return itertools.chain.from_iterable(xs)

def flatmap(f, xs):
    return flatten(map(f, xs))

def zipwith(f, *xss):
    return map(f, *xss)

def group_by(f, xs):
    it = iter(xs)
    last = next(it)
    group = [last]

    for x in it:
        if f(x, last):
            group.append(x)
        else:
            yield group
            group = [x]

        last = x

    if group:
        yield group

def group(xs):
    return group_by(operator.eq, xs)

def flip(f):
    return lambda y,x: f(x, y)

def compose(f, g):
    return lambda x: f(g(x))

def foldl(f, xs, init):
    return functools.reduce(f, xs, init)

def foldl1(f, xs):
    return functools.reduce(f, xs)

def foldr1(f, xs):
    # foldr1 f xs ~ foldl (flip f) (reverse xs)
    return functools.reduce(flip(f), reversed(xs))

def nub(xs):
    return list(set(xs))

def iterate(f, x):
    while True:
        yield x
        x = f(x)

def length(xs):
    if type(xs) in (list, str, dict):
        return len(xs)

    # count iterables
    n = 0
    for _ in xs: n += 1

    return n

def take(n, xs):
    return itertools.islice(xs, 0, n)

def drop(n, xs):
    return itertools.islice(xs, n, None)

def index(i, xs):
    """Index into any indexable object, including iterables."""

    if type(xs) in (list, str, dict, range):
        return xs[i]

    # index into an iterable
    it = iter(xs)
    try:
        for _ in range(i):
            next(it)
        return next(it)
    except StopIteration:
        raise IndexError("iterable index out of range")

def find(f, xs):
    for x in xs:
        if f(x):
            return x
    return None # TODO: except?

def find_index(f, xs):
    for i, x in enumerate(xs):
        if f(x):
            return i
    return None # TODO: except?

def partition(f, xs):
    it = iter(xs)

    first = []
    second = []

    for x in it:
        if f(x):
            first.append(x)
        else:
            second.append(x)
            break

    second.extend(list(it))
    return (first, second)