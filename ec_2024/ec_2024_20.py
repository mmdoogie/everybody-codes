from itertools import pairwise

import mrm.ansi_term as ansi
from mrm.dijkstra import dijkstra, Dictlike
from mrm.image import print_image
from mrm.point import grid_as_dict, adj_ortho

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid = grid_as_dict(lines, valid=lambda x: x != '#')
    return grid

def part1(output=False):
    grid = parse('data/ec_2024/20-a.txt')
    start = [k for k, v in grid.items() if v == 'S'][0]
    to_loop = [k for k, v in grid.items() if k[1] == 24 and v == '+' and (grid[(k[0] - 1, k[1])] == '+' or grid[(k[0] + 1, k[1])] == '+')]
    ngh = {g: adj_ortho(g, grid) for g in grid}

    def weights(segment):
        dst, _ = segment
        if grid[dst] == '-':
            return 3
        if grid[dst] == '.':
            return 2
        return 0

    wts, paths = dijkstra(ngh, Dictlike(weights), start_point=(start), end_point=to_loop)
    short = min((wts[l], paths[l]) for l in to_loop)
    dist_to_loop = len(short[1]) - 1
    alt_chg_to_loop = -(short[0] - dist_to_loop)

    if output:
        print('Dist to loop', dist_to_loop, ', alt change', alt_chg_to_loop)
        print_image(grid, use_char=True, default_char='#', highlighter=lambda x, y, c: ansi.red(c) if (x, y) in short[1] else c)

    return 1000 + alt_chg_to_loop + 100 - dist_to_loop

def part2(output=False):
    grid = parse('data/ec_2024/20-b.txt')
    key_pts = {v: k for k, v in grid.items() if v in 'SABC'}

    def neighbors(state):
        dst, src = state
        ngh = [(a, dst) for a in adj_ortho(dst, grid) if a != src]
        return ngh

    def weights(segment):
        _, to_st = segment
        dst, _ = to_st
        if grid[dst] == '-':
            return 3
        if grid[dst] in '.ABCS':
            return 2
        return 0

    full_path = []
    seg = {}
    dist = 0
    curr_start = (key_pts['S'], None)
    for a, b in pairwise('SABCS'):
        wts, paths = dijkstra(Dictlike(neighbors), Dictlike(weights), start_point=curr_start, end_point=[(key_pts[b], d) for d in adj_ortho(key_pts[b], grid)])
        which_b = min((wts[w], paths[w][1:]) for w in wts if w[0] == key_pts[b])
        full_path += [p[0] for p in which_b[1]]
        seg.update({p[0]: b for p in which_b[1]})
        curr_start = which_b[1][-1]
        dist += -(which_b[0] - len(which_b[1]))

    if output:
        print('Path length', len(full_path), ', alt change', dist)
        colors = {'A': ansi.red, 'B': ansi.green, 'C': ansi.blue, 'S': ansi.magenta}
        print_image(grid, use_char=True, default_char='#', highlighter=lambda x, y, c: colors[seg[(x, y)]](c) if (x, y) in seg else c)

    return len(full_path) - min(dist, 0)

def part3(output=False):
    grid = parse('data/ec_2024/20-c.txt')
    start = [k for k, v in grid.items() if v == 'S'][0]
    max_y = max(p[1] for p in grid)
    bottom = [k for k in grid if k[1] == max_y]

    def neigh(state):
        dst, src = state
        ngh = [(a, dst) for a in adj_ortho(dst, grid) if a != src]
        return ngh

    def weights(segment):
        _, to_st = segment
        dst, _ = to_st
        if grid[dst] == '-':
            return 2
        if grid[dst] == '.':
            return 1
        return -1

    wts, paths = dijkstra(Dictlike(neigh), Dictlike(weights), start_point=(start, None), end_point=[(b, a) for b in bottom for a in adj_ortho(b, grid)])
    which_b = min((wts[w], paths[w][1:], w) for w in wts if w[0] in bottom)
    sel_path = [p[0] for p in which_b[1]]
    dist = which_b[0]

    sb_steps = max_y
    sb_chg = dist
    sb_end = (which_b[2][0][0], -1)

    if output:
        print('Start-to-bottom')
        print('South steps', max_y, 'alt change', dist)
        print_image(grid, use_char=True, default_char='#', highlighter=lambda x, y, c: ansi.red(c) if (x, y) in sel_path else c)

    wts, paths = dijkstra(Dictlike(neigh), Dictlike(weights), start_point=(sb_end, None), end_point=[(b, a) for b in bottom for a in adj_ortho(b, grid)])
    which_b = min((wts[w], paths[w][1:], w) for w in wts if w[0] in bottom)
    sel_path = [p[0] for p in which_b[1]]
    dist = which_b[0]

    if output:
        print('Repeat #1')
        print('South steps', max_y + 1, 'alt change', dist)
        print_image(grid, use_char=True, default_char='#', highlighter=lambda x, y, c: ansi.red(c) if (x, y) in sel_path else c)

    assert which_b[2][0][0] == sb_end[0]
    remain = (384400 - sb_chg) % dist
    extra_steps = 0
    for p in sel_path:
        remain -= weights((None, (p, None)))
        extra_steps += 1
        if remain <= 0:
            break

    if output:
        print('Alt remaining', (384400 - sb_chg) % dist, 'final steps', extra_steps)

    return sb_steps + ((384400 - sb_chg) // dist) * (max_y + 1) + extra_steps
