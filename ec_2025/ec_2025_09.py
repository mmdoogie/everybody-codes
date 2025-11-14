from collections import defaultdict
from functools import partial

from mrm.graph import connected_component

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    lines = [l.split(':') for l in lines]
    return {int(l[0]): l[1] for l in lines}

def find_parents(has_letter_at, dnas, dnak):
    child = dnas[dnak]
    cand_1 = has_letter_at[child[0]][0]
    for pp1 in cand_1:
        if pp1 == dnak:
            continue
        i = 0
        while pp1 in has_letter_at[child[i]][i]:
            i += 1
        cand_2 = has_letter_at[child[i]][i]
        for pp2 in cand_2:
            if pp2 == dnak:
                continue
            sc1 = i
            sc2 = 0
            for j, c in enumerate(child[i:]):
                match = False
                if pp1 in has_letter_at[c][j+i]:
                    sc1 += 1
                    match = True
                if pp2 in has_letter_at[c][j+i]:
                    sc2 += 1
                    match = True
                if not match:
                    break
            else:
                sc2 += sum(a==b for a,b in zip(child[:i], dnas[pp2]))
                return min(pp1, pp2), max(pp1, pp2), sc1 * sc2
    return None, None, 0

def compute_sets(dnas):
    has_letter_at = defaultdict(partial(defaultdict, set))
    for dn, dv in dnas.items():
        for i, c in enumerate(dv):
            has_letter_at[c][i].add(dn)
    return has_letter_at

def part1(output=False):
    dnas = parse('data/ec_2025/09-a.txt')
    has_letter_at = compute_sets(dnas)

    for pch in dnas:
        _, _, sc = find_parents(has_letter_at, dnas, pch)
        if sc:
            return sc

    return 0

def part2(output=False):
    dnas = parse('data/ec_2025/09-b.txt')
    has_letter_at = compute_sets(dnas)

    tot = sum(find_parents(has_letter_at, dnas, pch)[2] for pch in dnas)

    return tot

def part3(output=False):
    dnas = parse('data/ec_2025/09-c.txt')
    has_letter_at = compute_sets(dnas)

    ngh = defaultdict(set)
    for pch in dnas:
        p1, p2, _ = find_parents(has_letter_at, dnas, pch)
        if not p1:
            continue
        ngh[pch].update([p1, p2])
        ngh[p1].update([pch, p2])
        ngh[p2].update([pch, p1])

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
