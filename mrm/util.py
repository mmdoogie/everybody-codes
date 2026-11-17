"""Module for small helper functions without a home"""

__all__ = ['big_pi', 'fastreverse_deque', 'Funkydict', 'md5sum', 'product', 'repeatedly_apply']

from collections import deque, UserDict
from functools import reduce
from hashlib import md5
from operator import mul

def md5sum(s):
    """Provides the hex-encoded MD5 hash of a string"""
    return md5(s.encode('utf-8')).hexdigest()

def product(x):
    """Multiplies all elements of an iterable together"""
    return reduce(mul, x)

big_pi = product

class Funkydict(UserDict):
    """Dict-like object that immediately applies a reducing function when items are set

    initial_data: data to load prior to operation
    set_fun: function taking current and new value and returning reduced/accumulated value to store
    defaultfactory: function to create the base value for new keys
    """

    def __init__(self, initialdata = None, set_fun = lambda curr, new: new, default_factory = int):
        if initialdata:
            super().__init__(initialdata)
        self.set_fun = set_fun
        self.default_factory = default_factory

    def __setitem__(self, key, val):
        if key in self:
            curr = self[key]
        else:
            curr = self.default_factory()
        self.data[key] = self.set_fun(curr, val)

def repeatedly_apply(fn, iv, times, *args, **kwargs):
    """Repeatedly apply a function to it's previous value"""
    val = iv
    for _ in range(times):
        val = fn(val, *args, **kwargs)
    return val

class fastreverse_deque:
    """deque-like object that uses a flag to swap left/right append/pop operations
    instead of reordering the values in memory. Only some operations are implemented.
    """

    def __init__(self, iterable=[]):
        self._rev_flag = False
        self._data = deque(iterable)

    def reverse(self):
        self._rev_flag = not self._rev_flag

    def __bool__(self):
        return bool(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, idx):
        if self._rev_flag:
            return self._data[-idx-1]
        return self._data[idx]

    def __repr__(self):
        return repr(self._data)

    def append(self, value):
        if self._rev_flag:
            self._data.appendleft(value)
        self._data.append(value)

    def appendleft(self, value):
        if self._rev_flag:
            self._data.append(value)
        self._data.appendleft(value)

    def clear(self):
        self._data.clear()
        self._rev_flag = False

    def pop(self):
        if self._rev_flag:
            return self._data.popleft()
        return self._data.pop()

    def popleft(self):
        if self._rev_flag:
            return self._data.pop()
        return self._data.popleft()


