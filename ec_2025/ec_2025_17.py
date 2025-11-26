from collections import defaultdict
from functools import cache
import math
import mrm.ansi_term as ansi
from mrm.dijkstra import Dictlike, dijkstra
from mrm.parse import int_if_possible
import mrm.point as pt
import mrm.image as img

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid, grid_inv = pt.grid_as_dict(lines, with_inv=True, conv=int_if_possible)
    if 'S' in grid_inv:
        return grid, grid_inv['@'].pop(), grid_inv['S'].pop()
    return grid, grid_inv['@'].pop()

def part1(output=False):
    grid, volcano = parse('data/ec_2025/17-a.txt')

    tot = 0
    for (x, y), c in grid.items():
        if c == '@':
            continue
        if (x - volcano[0])**2 + (y - volcano[1])**2 <= 10**2:
            tot += int(c)

    if output:
        def hl(x, y, c):
            if (x - volcano[0])**2 + (y - volcano[1])**2 <= 10**2:
                return c
            return '.'
        img.print_image(grid, True, highlighter=hl)

    return tot

def part2(output=False):
    grid, volcano = parse('data/ec_2025/17-b.txt')

    tots = defaultdict(int)
    for (x, y), c in grid.items():
        if c == '@':
            continue
        r_sq = (x - volcano[0])**2 + (y - volcano[1])**2
        r = math.ceil(math.sqrt(r_sq))
        tots[r] += c

    r, tot = max(tots.items(), key=lambda x: x[1])

    if output:
        def hl(x, y, c):
            if (x - volcano[0])**2 + (y - volcano[1])**2 <= r**2:
                return c
            return '.'
        img.print_image(grid, True, highlighter=hl)

    return r * tot

def part3(output=False):
    grid, volcano, start = parse('data/ec_2025/17-c.txt')

    @cache
    def pt_rad(p):
        x, y = p
        return math.ceil(math.sqrt((x - volcano[0])**2 + (y - volcano[1])**2))

    curr_rad = 10
    while True:
        curr_rad += 1
        time_limit = 30 * (curr_rad + 1)

        side = 1
        def adj(p):
            cand = pt.adj_ortho(p, grid)
            return [c for c in cand if pt_rad(c) > curr_rad and side*c[0] < side*volcano[0] + 10]
        ngh = Dictlike(adj)
        wts = Dictlike(lambda pp: grid[pp[1]] if pp[1] != start else 0)
        end_pts = [(volcano[0], volcano[1] + curr_rad + 1 + i) for i in range(10)]

        left_wt, left_path = dijkstra(ngh, wts, start, end_pts)
        if min(left_wt[e] for e in end_pts) > time_limit:
            continue

        side = -1
        right_wt, right_path = dijkstra(ngh, wts, start, end_pts)
        total_wts = [left_wt[e] + right_wt[e] - grid[e] for e in end_pts]
        if min(total_wts) > time_limit:
            continue

        if output:
            def hl(x, y, c):
                p = (x, y)
                c = str(c)
                if pt_rad(p) <= curr_rad:
                    return '.'
                if p in left_path[end_pts[0]]:
                    return ansi.red(c)
                if p in right_path[end_pts[0]]:
                    return ansi.green(c)
                if p in end_pts:
                    return ansi.blue(c)
                return c
            img.print_image(grid, True, highlighter=hl)

        break

    return min(total_wts) * curr_rad
