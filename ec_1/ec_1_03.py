from mrm.parse import all_nums
from mrm.crt import crt

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return [list(all_nums(l)) for l in lines]

def from_diag(x, y):
    disc = y + x - 1
    offset = x - 1

    return disc, offset

def to_diag(disc, offset):
    x = offset + 1
    y = disc - x + 1

    return x, y

def part1(output=False):
    lines = parse('data/ec_1/03-a.txt')
    tot = 0
    for l in lines:
        x, y = l
        d, o = from_diag(x, y)
        npos = (o + 100) % d
        x, y = to_diag(d, npos)
        tot += x + 100 * y

    return tot

def part2(output=False):
    lines = parse('data/ec_1/03-b.txt')
    vals = []
    mods = []

    for l in lines:
        x, y = l
        d, o = from_diag(x, y)
        mods += [d]
        vals += [d - 1 - o]

    n = crt(vals, mods)

    return n

def part3(output=False):
    lines = parse('data/ec_1/03-c.txt')
    vals = []
    mods = []

    for l in lines:
        x, y = l
        d, o = from_diag(x, y)
        mods += [d]
        vals += [d - 1 - o]

    n = crt(vals, mods)

    return n
