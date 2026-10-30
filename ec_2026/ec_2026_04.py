from collections import defaultdict
from functools import partial

from mrm.parse import all_nums

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse('data/ec_2026/04-a.txt')
    times = defaultdict(int)
    for l in lines:
        i, _, _, t = list(all_nums(l))
        times[i] += t
    rank = sorted(times.values())
    chk = sum(i * r for i, r in enumerate(rank, start=1))
    return chk

def part2(output=False):
    lines = parse('data/ec_2026/04-b.txt')
    times = defaultdict(partial(list, [0, 0]))
    for l in lines:
        i, _, _, t = list(all_nums(l))
        times[i][0] -= 1
        times[i][1] += t
    rank = sorted(times.values())
    chk = sum(i * r[1] for i, r in enumerate(rank, start=1))
    return chk

class DupeRank:
    def __init__(self, start, incr):
        self._incr = incr
        self._accum = incr
        self._prev = None
        self._rank = start

    def next_rank(self, val):
        if self._prev and self._prev == val:
            self._accum += self._incr
        elif self._prev:
            self._rank += self._accum
            self._accum = self._incr
        self._prev = val
        if self._rank <= 0:
            return 0
        return self._rank

def part3(output=False):
    lines = parse('data/ec_2026/04-c.txt')
    qpt = defaultdict(partial(defaultdict, dict))
    for l in lines:
        i, q, p, t = list(all_nums(l))
        qpt[q][p][i] = t

    for q in qpt:
        for i in qpt[q][2]:
            qpt[q][2][i] += qpt[q][1][i]
        for i in qpt[q][3]:
            qpt[q][3][i] += qpt[q][2][i]

    points = defaultdict(int)
    for q in qpt:
        for p in qpt[q]:
            tms = sorted(qpt[q][p].items(), key=lambda x:x[1])
            d = DupeRank(50 * p, -1)
            for i, t in tms:
                points[i] += d.next_rank(t)

    scores = sorted(points.values(), reverse=True)
    d = DupeRank(1, 1)
    chk = sum(s * d.next_rank(s) for s in scores)
    return chk
