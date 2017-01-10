# darkf.py -- a supplemental standard library by darkf
# Copyright (c) 2017 darkf -- licensed under the terms of the MIT license
#
# NOTE: _ will have to be imported explicitly, if desired.

import itertools

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
    return list(itertools.chain.from_iterable(xs))

def flatmap(f, xs):
    return flatten(map(f, xs))
