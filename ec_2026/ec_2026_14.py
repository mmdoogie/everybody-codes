from collections import defaultdict
from itertools import combinations
import math

from mrm.graph import prim_mst
import mrm.point as pt

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid = pt.grid_as_dict(lines)
    ngh = defaultdict(set)
    wts = defaultdict(int)
    for g in grid:
        for n in pt.adj_ortho(g):
            if n not in grid:
                gn = ' '
            else:
                gn = grid[n]
            gg = grid[g]

            if gn != gg:
                ngh[gg].add(gn)
                ngh[gn].add(gg)
                wts[(gg, gn)] += 1
                wts[(gn, gg)] += 1
    for w in wts:
        if ' ' not in w:
            wts[w] //= 2
    return ngh, wts

def part1(output=False):
    _, wts = parse('data/ec_2026/14-a.txt')

    return sum(wts.values()) // 2

def part2(output=False):
    ngh, wts = parse('data/ec_2026/14-b.txt')

    _, edges = prim_mst(ngh, wts)

    return sum(wts[e] for e in edges)

def part3(output=False):
    ngh, wts = parse('data/ec_2026/14-c.txt')

    min_score = math.inf
    for i1, i2 in combinations(ngh, 2):
        if i1 == ' ' or i2 == ' ':
            continue

        copy_wts = dict(wts.items())
        for w in copy_wts:
            if i1 in w or i2 in w:
                copy_wts[w] = 0
        _, edges = prim_mst(ngh, copy_wts)

        score = sum(copy_wts[e] for e in edges)
        min_score = min(min_score, score)

    return min_score
