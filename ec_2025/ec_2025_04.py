from fractions import Fraction
from itertools import pairwise
from math import floor, ceil

from mrm.parse import all_nums

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse('data/ec_2025/04-a.txt')
    gears = [int(x) for x in lines]

    ratio = Fraction(1)
    for a, b in pairwise(gears):
        ratio = ratio * a / b

    return floor(ratio * 2025)

def part2(output=False):
    lines = parse('data/ec_2025/04-b.txt')
    gears = [int(x) for x in lines]

    ratio = Fraction(1)
    for a, b in pairwise(gears):
        ratio = ratio * a / b

    return ceil(10000000000000 / ratio)

def part3(output=False):
    lines = parse('data/ec_2025/04-c.txt')
    gears = [list(all_nums(x)) for x in lines]
    gears[0] = [0] + gears[0]

    ratio = Fraction(1)
    for a, b in pairwise(gears):
        ratio = ratio * a[1] / b[0]

    return floor(ratio * 100)
