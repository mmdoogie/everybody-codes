from collections import defaultdict
from itertools import combinations

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    num_portals = int(lines[0].split(' ')[1])
    shortcuts = [[int(x) for x in l.split(' ')] for l in lines[2:]]
    return num_portals, shortcuts

def dists(adj, start):
    horizon = set([start])
    depth = 0
    dist = {start: depth}
    while horizon:
        depth += 1
        next_horizon = set()
        for h in horizon:
            for a in adj[h]:
                if a in dist:
                    continue
                next_horizon.add(a)
                dist[a] = depth
        horizon = next_horizon
    return dist

def part1(output=False):
    num_portals, shortcuts = parse('data/ec_2026/11-a.txt')

    adj = defaultdict(set)
    for n in range(num_portals):
        adj[n].add((n + 1) % num_portals)
        adj[n].add((n - 1) % num_portals)

    pre_score = 0
    for s in range(num_portals):
        d = dists(adj, s)
        pre_score += sum(d.values())

    for fm, to in shortcuts:
        adj[fm - 1].add(to - 1)
        adj[to - 1].add(fm - 1)

    post_score = 0
    for s in range(num_portals):
        d = dists(adj, s)
        post_score += sum(d.values())

    return pre_score - post_score

def part2(output=False):
    num_portals, shortcuts = parse('data/ec_2026/11-b.txt')

    adj = defaultdict(set)
    for n in range(num_portals):
        adj[n].update((n + i) % num_portals for i in range(-3, 4) if i != 0)

    pre_score = 0
    for s in range(num_portals):
        d = dists(adj, s)
        pre_score += sum(d.values())

    for fm, to in shortcuts:
        adj[fm - 1].add(to - 1)
        adj[to - 1].add(fm - 1)

    max_resonance = 0
    for tc1, tc2 in combinations(range(num_portals), 2):
        if tc2 in adj[tc1]:
            continue

        adj[tc1].add(tc2)
        adj[tc2].add(tc1)

        post_score = 0
        for s in range(num_portals):
            d = dists(adj, s)
            post_score += sum(d.values())
        resonance = pre_score - post_score
        if output:
            print(f'TC Conn {tc1:2} -> {tc2:2} resonance {resonance}', end='')

        adj[tc1].remove(tc2)
        adj[tc2].remove(tc1)

        if resonance > max_resonance:
            max_resonance = resonance
            if output:
                print(' *')
        elif output:
            print()

    return max_resonance

def part3(output=False):
    num_portals, shortcuts = parse('data/ec_2026/11-c.txt')

    adj = defaultdict(set)
    for n in range(num_portals):
        adj[n].update((n + i) % num_portals for i in range(-3, 4) if i != 0)

    pre_score = 0
    for s in range(num_portals):
        d = dists(adj, s)
        pre_score += sum(d.values())

    for fm, to in shortcuts:
        adj[fm - 1].add(to - 1)
        adj[to - 1].add(fm - 1)

    patterns = set()
    s1 = list(range(8))
    for ab in combinations(s1, 2):
        s2 = [x for x in s1 if x not in ab]
        for cd in combinations(s2, 2):
            s3 = [x for x in s2 if x not in cd]
            for ef in combinations(s3, 2):
                gh = [x for x in s3 if x not in ef]
                parts = [tuple(sorted(ab)), tuple(sorted(cd)), tuple(sorted(ef)), tuple(sorted(gh))]
                patterns.add(tuple(sorted(parts)))

    max_resonance = 0
    remain = len(patterns) * (num_portals // 8)
    for offset in range(num_portals // 8):
        tcs = [offset + i * (num_portals // 8) for i in range(8)]
        for p in patterns:
            adj_copy = {k: set(v) for k, v in adj.items()}
            for a, b in p:
                adj_copy[tcs[a]].add(tcs[b])
                adj_copy[tcs[b]].add(tcs[a])
            post_score = 0
            for s in range(num_portals):
                d = dists(adj_copy, s)
                post_score += sum(d.values())
            remain -= 1
            max_resonance = max(max_resonance, pre_score - post_score)
            if output and remain % 10 == 0:
                print(f'Remaining patterns: {remain:4} max resonance: {max_resonance}')

    return max_resonance
