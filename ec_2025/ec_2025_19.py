from collections import defaultdict
from functools import partial
from itertools import pairwise

import mrm.ansi_term as ansi
from mrm.dijkstra import Dictlike, dijkstra
from mrm.parse import all_nums

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    nums = [list(all_nums(l)) for l in lines]
    triplets = defaultdict(list)
    for n in nums:
        x, y, cnt = n
        triplets[x] += [range(y, y+cnt)]
    return triplets

def simple_ngh(triplets, p):
    x,y = p
    if x == max(triplets):
        return []

    cand = [(x+1, y+1)]
    if y > 1:
        cand += [(x+1, y-1)]

    return [(cx, cy) for cx, cy in cand if cx not in triplets or any(cy in r for r in triplets[cx])]

def simple_wt(pp):
    (_, y1), (_, y2) = pp
    return 1 if y2 > y1 else 0

def draw_path(triplets, path):
    max_x = max(triplets)
    max_y = max(max(rr) for r in triplets.values() for rr in r)

    chars = {b: '^' if b[1]>a[1] else 'v' for a, b in pairwise(path)}
    chars[(0,0)] = '@'

    for y in range(max_y + 1, -1-1, -1):
        for x in range(max_x + 1):
            if y == max_y + 1:
                print(ansi.blue('~'), end='')
                continue
            if y == -1:
                print(ansi.green('~'), end='')
                continue
            if x in triplets and all(y not in r for r in triplets[x]):
                print(ansi.red('#'), end='')
            else:
                if (x, y) in path:
                    print(ansi.yellow(chars[(x, y)]), end='')
                else:
                    print(' ', end='')
        print()

def part1(output=False):
    triplets = parse('data/ec_2025/19-a.txt')

    wts, paths = dijkstra(Dictlike(partial(simple_ngh, triplets)), Dictlike(simple_wt), (0, 0))
    win = min((wv, wk) for wk, wv in wts.items() if wk[0] == max(triplets))

    if output:
        draw_path(triplets, paths[win[1]])

    return win[0]

def part2(output=False):
    triplets = parse('data/ec_2025/19-b.txt')

    wts, paths = dijkstra(Dictlike(partial(simple_ngh, triplets)), Dictlike(simple_wt), (0, 0))
    win = min((wv, wk) for wk, wv in wts.items() if wk[0] == max(triplets))

    if output:
        draw_path(triplets, paths[win[1]])

    return win[0]

def part3(output=False):
    triplets = parse('data/ec_2025/19-c.txt')
    next_wall = dict(pairwise(sorted(triplets)))
    next_wall[0] = min(triplets)

    seen_x = {}
    def ngh(p):
        x, y = p
        if x == max(triplets):
            return []

        nx = next_wall[x]
        cand = []
        for r in triplets[nx]:
            for ny in r:
                dd = ny-y + nx-x
                if dd % 2 != 0:
                    continue
                if 0 <= dd//2 <= nx-x:
                    cand += [(nx, ny)]

        if nx not in seen_x:
            seen_x[nx] = True
            if output:
                print(f'At wall {nx}')

        return cand

    def wt(pp):
        (x1, y1), (x2, y2) = pp
        dd = y2-y1 + x2-x1
        return dd//2

    wts = dijkstra(Dictlike(ngh), Dictlike(wt), (0, 0), keep_paths=False)

    return min(wts[w] for w in wts if w[0] == max(triplets))
