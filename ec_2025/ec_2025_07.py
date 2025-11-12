from collections import defaultdict
from itertools import combinations, pairwise

from mrm.dijkstra import Dictlike
from mrm.graph import bfs_dist

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    names = lines[0].split(',')
    rules = defaultdict(set)
    for l in lines[2:]:
        lh, rh = l.split(' > ')
        rh = rh.split(',')
        rules[lh].update(rh)
    return names, rules

def part1(output=False):
    names, rules = parse('data/ec_2025/07-a.txt')

    for n in names:
        for a, b in pairwise(n):
            if b not in rules[a]:
                break
        else:
            return n

    return ''

def part2(output=False):
    names, rules = parse('data/ec_2025/07-b.txt')

    ok_names = 0
    for i, n in enumerate(names):
        for a, b in pairwise(n):
            if b not in rules[a]:
                break
        else:
            ok_names += (i + 1)

    return ok_names

def part3(output=False):
    names, rules = parse('data/ec_2025/07-c.txt')

    ok_names = set()
    for n in names:
        for a, b in pairwise(n):
            if b not in rules[a]:
                break
        else:
            ok_names.add(n)

    included_names = set()
    for a, b in combinations(ok_names, 2):
        if a in b:
            included_names.add(b)
        if b in a:
            included_names.add(a)

    ngh = Dictlike(lambda x: {x + nxt for nxt in rules[x[-1]]})
    total_names = 0
    for n in ok_names - included_names:
        name_len = len(n)
        names = bfs_dist(ngh, n, 11 - name_len)
        for p in names.prios():
            if p >= 7 - name_len:
                total_names += len(names[p])

    return total_names
