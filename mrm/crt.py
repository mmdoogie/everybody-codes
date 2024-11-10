from functools import reduce
from itertools import combinations
from operator import mul
from math import gcd

def crt(vals, mods):
    for a, b in combinations(mods, 2):
        if gcd(a, b) != 1:
            raise ValueError(f'GCD of {a} and {b} != 1')

    mod_prod = reduce(mul, mods)
    isolates = [mod_prod // m for m in mods]

    factors = []
    for iso, mod, val in zip(isolates, mods, vals):
        if iso % mod == val:
            factors += [1]
            continue
        f = 2
        while (iso * f) % mod != val:
            f += 1
        factors += [f]

    test_val = sum(iso * fact for iso, fact in zip(isolates, factors))
    while test_val > mod_prod:
        test_val -= mod_prod

    return test_val
