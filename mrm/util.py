from functools import reduce
from hashlib import md5
from operator import mul

def md5sum(s):
    return md5(s.encode('utf-8')).hexdigest()

def product(x):
    return reduce(mul, x)
