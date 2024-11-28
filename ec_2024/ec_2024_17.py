from collections import defaultdict
from itertools import product

from mrm.graph import prim_mst
from mrm.point import grid_as_dict, m_dist
from mrm.util import big_pi

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output):
    lines = parse('data/ec_2024/17-a.txt')
    g = grid_as_dict(lines, valid=lambda x:x=='*')
    weights = {(s, d): m_dist(s, d) for s, d in product(g, repeat=2)}
    ngh = {s: list(g.keys()) for s in g}
    nodes, edges = prim_mst(ngh, weights)
    return sum(weights[e] for e in edges) + len(nodes)

def part2(output):
    lines = parse('data/ec_2024/17-b.txt')
    g = grid_as_dict(lines, valid=lambda x:x=='*')
    weights = {(s, d): m_dist(s, d) for s, d in product(g, repeat=2)}
    ngh = {s: list(g.keys()) for s in g}
    nodes, edges = prim_mst(ngh, weights)
    return sum(weights[e] for e in edges) + len(nodes)

def part3(output):
    lines = parse('data/ec_2024/17-c.txt')
    g = grid_as_dict(lines, valid=lambda x:x=='*')
    weights = {}
    ngh = defaultdict(list)
    for s, d in product(g, repeat=2):
        dist = m_dist(s, d)
        weights[(s, d)] = dist
        if dist < 6 and s != d:
            ngh[s] += [d]
            ngh[d] += [s]

    remain = set(g)
    sizes = []

    while remain:
        seed = remain.pop()
        nodes, edges = prim_mst(ngh, weights, seed)
        sizes += [sum(weights[e] for e in edges) + len(nodes)]
        remain.difference_update(nodes)

    return big_pi(sorted(sizes, reverse=True)[:3])
