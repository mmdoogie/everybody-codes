from collections import defaultdict

from mrm.dijkstra import dijkstra
import mrm.point as pt

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid, inv_grid = pt.grid_as_dict(lines, lambda x: x in 'TSE', True)
    if 'S' in inv_grid and 'E' in inv_grid:
        return grid, inv_grid['S'].pop(), inv_grid['E'].pop(), len(lines[0])
    return grid

def part1(output=False):
    grid = parse('data/ec_2025/20-a.txt')

    sbs = 0
    for g in grid:
        if (g[0] + 1, g[1]) in grid:
            sbs += 1
        if g[0] % 2 == g[1] % 2:
            continue
        if (g[0], g[1] + 1) in grid:
            sbs += 1

    return sbs

def part2(output=False):
    grid, sp, ep, _ = parse('data/ec_2025/20-b.txt')

    adj = defaultdict(list)
    for g in grid:
        rn = (g[0] + 1, g[1])
        if rn in grid:
            adj[g] += [rn]
            adj[rn] += [g]
        if g[0] % 2 == g[1] % 2:
            continue
        dn = (g[0], g[1] + 1)
        if dn in grid:
            adj[g] += [dn]
            adj[dn] += [g]

    wt = dijkstra(adj, start_point=sp, end_point=ep, keep_paths=False)

    return wt[ep]

def rotate_grid(grid, grid_width):
    new_grid = {}
    for y in range(grid_width):
        curr_x, curr_y = 2*y, 0
        while curr_x <= grid_width-1 and curr_y <= grid_width-1:
            if (curr_x, curr_y) in grid:
                new_x = y + grid_width-1 - curr_x - curr_y
                new_grid[(new_x, y)] = grid[(curr_x, curr_y)]
            curr_x += 1
            if curr_x > grid_width-1:
                break
            if (curr_x, curr_y) in grid:
                new_x = y + grid_width-1 - curr_x - curr_y
                new_grid[(new_x, y)] = grid[(curr_x, curr_y)]
            curr_y += 1
    return new_grid

def make_adj(grids):
    adj = defaultdict(list)

    for gn, grid in grids.items():
        ngn = (gn + 1) % 3
        for g in grid:
            x, y = g
            if (x + 1, y) in grids[ngn]:
                adj[(*g, gn)] += [(x + 1, y, ngn)]

            if (x - 1, y) in grids[ngn]:
                adj[(*g, gn)] += [(x - 1, y, ngn)]

            if (x, y) in grids[ngn]:
                adj[(*g, gn)] += [(x, y, ngn)]

            if x % 2 == y % 2:
                if (x, y - 1) in grids[ngn]:
                    adj[(*g, gn)] += [(x, y - 1, ngn)]
            else:
                if (x, y + 1) in grids[ngn]:
                    adj[(*g, gn)] += [(x, y + 1, ngn)]

    return adj

def part3(output=False):
    grid, sp, _, grid_width = parse('data/ec_2025/20-c.txt')

    grids = {0: grid}
    grids[1] = rotate_grid(grid, grid_width)
    grids[2] = rotate_grid(grids[1], grid_width)
    eps = []
    for gn, g in grids.items():
        for gp, gc in g.items():
            if gc == 'E':
                eps += [(*gp, gn)]
                break
    adj = make_adj(grids)

    wt = dijkstra(adj, start_point=(*sp, 0), end_point=eps, keep_paths=False)

    return min(wt[e] for e in eps if e in wt)
