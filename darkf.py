# darkf.py -- a supplemental standard library by darkf
# Copyright (c) 2017 darkf -- licensed under the terms of the MIT license
#
# NOTE: _ will have to be imported explicitly, if desired.

# TODO: Make a lot of these iterable functions work nicely on strings
# such that if the input is a string, produce a string as output.

import itertools, functools, operator

class UnderscoreProxy:
    """A proxy object that returns accessors for attributes and
       items looked up on it.

       Example: _.foo is the same as lambda x: x.foo
                _["foo"] is the same as lambda x: x["foo"]

       It is useful for producing higher-order functions with nicer
       syntax than operator.itemgetter.
    """

    # TODO: Add operator syntax for lambdas, e.g. _ == 3 meaning `lambda x: x == 3`
    # as well as for item accessors, e.g. `_.foo == 3`.

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

def xmap(f, xs):
    """Map returning a list."""
    return list(map(f, xs))

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

def scanl1(f, xs):
    return itertools.accumulate(xs, f)

def product(xs):
    return functools.reduce(operator.mul, xs)

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

def transpose(xs):
    """Transpose a list matrix."""
    return list(map(list, zip(*xs)))

def cons(x, xs):
    ys = [x]
    ys.extend(xs)
    return ys

def uncons(xs):
    return (head(xs), tail(xs))

def head(xs): return next(iter(xs))
def tail(xs): return drop(1, xs)
def empty(xs): return length(xs) == 0

def lines(s): return s.split("\n")
def unlines(xs): return "\n".join(xs)

def words(s): return s.split()
def unwords(xs): return " ".join(xs)

def fst(pair): return pair[0]
def snd(pair): return pair[1]

def mapfst(f, pair):
    return (f(pair[0]), pair[1])

def mapsnd(f, pair):
    return (pair[0], f(pair[1]))

def swap_pair(pair):
    (a, b) = pair
    return (b, a)

class BiMap:
    """A bi-directional map (dict). Key map to values and values to keys."""

    def __init__(self, *args, **kwargs):
        self.fwd = dict(*args, **kwargs)
        self.bwd = dict(map(swap_pair, self.fwd.items()))

    def __len__(self): return len(self.fwd) + len(self.bwd)
    def __getitem__(self, key):
        if key in self.fwd:
            return self.fwd[key]
        elif key in self.bwd:
            return self.bwd[key]
        raise KeyError(key)

    def __setitem__(self, key, value):
        if key in self.fwd:
            # remove old bwd reference
            del self.bwd[self.fwd[key]]
        
        self.fwd[key] = value
        self.bwd[value] = key

    def __contains__(self, key): return key in self.fwd or key in self.bwd

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self):
        self.fwd.clear()
        self.bwd.clear()

    def items(self):
        return flatten((self.fwd.items(), self.bwd.items()))

    def __iter__(self): return iter(self.items())

    def keys(self):
        return map(fst, self.items())

    def values(self):
        return map(snd, self.items())

    def update(self, other):
        self.fwd.update(other)
        self.bwd.update(map(swap_pair, other.items()))

    def copy(self):
        return BiMap(self.items())
