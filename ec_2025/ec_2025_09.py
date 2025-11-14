from collections import defaultdict
from itertools import combinations

from mrm.graph import connected_component

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    lines = [l.split(':') for l in lines]
    return {int(l[0]): l[1] for l in lines}

def det_child(dnas, ia, ib, ic):
    a, b, c = dnas[ia], dnas[ib], dnas[ic]
    is_a, is_b, is_c = True, True, True
    sc_ab, sc_ac, sc_bc = 0, 0, 0

    for aa, bb, cc in zip(a, b, c):
        if aa == bb:
            sc_ab += 1
        if aa == cc:
            sc_ac += 1
        if bb == cc:
            sc_bc += 1
        if aa != bb and aa != cc:
            is_a = False
        if bb != aa and bb != cc:
            is_b = False
        if cc != aa and cc != bb:
            is_c = False
        if not is_a and not is_b and not is_c:
            return None, 0, 0, 0
    if is_a:
        return ia, min(ib, ic), max(ib, ic), sc_ab * sc_ac
    if is_b:
        return ib, min(ia, ic), max(ia, ic), sc_ab * sc_bc
    if is_c:
        return ic, min(ia, ib), max(ia, ib), sc_ac * sc_bc
    return None, 0, 0, 0

def part1(output=False):
    dnas = parse('data/ec_2025/09-a.txt')

    _, _, _, sc = det_child(dnas, *dnas)

    return sc

def part2(output=False):
    dnas = parse('data/ec_2025/09-b.txt')

    parents = {}
    for p in combinations(dnas, 3):
        ch, p1, p2, sc = det_child(dnas, *p)
        if not ch:
            continue
        parents[ch] = (p1, p2, sc)

    tot = sum(v[2] for v in parents.values())

    return tot

def part3(output=False):
    dnas = parse('data/ec_2025/09-c.txt')

    parents = {}
    ngh = defaultdict(set)
    for p in combinations(dnas, 3):
        ch, p1, p2, sc = det_child(dnas, *p)
        if not ch:
            continue
        parents[ch] = (p1, p2, sc)
        ngh[ch].update([p1, p2])
        ngh[p1].update([ch, p2])
        ngh[p2].update([ch, p1])

    max_cmp = 0
    the_cmp = 0
    all_nodes = set(dnas)
    at = all_nodes.pop()
    while all_nodes:
        cc = connected_component(ngh, at)
        if len(cc) > max_cmp:
            max_cmp = len(cc)
            the_cmp = cc
        all_nodes.difference(cc)
        at = all_nodes.pop()

    return sum(the_cmp)
