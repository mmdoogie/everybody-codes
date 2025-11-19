import mrm.ansi_term as ansi
from mrm.dijkstra import Dictlike, dijkstra
import mrm.image as img
import mrm.point as pt

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse('data/ec_2025/12-a.txt')

    g = pt.grid_as_dict(lines)
    def adj(p):
        cand = pt.adj_ortho(p, g)
        return {c for c in cand if g[p] >= g[c]}
    ngh = Dictlike(adj)

    reach = dijkstra(ngh, start_point=(0, 0), keep_paths=False)

    if output:
        def color(x, y, c):
            opt = (x, y)
            if opt in reach:
                return ansi.red(c)
            return c
        img.print_image(g, use_char=True, highlighter=color)

    return len(reach)

def part2(output=False):
    lines = parse('data/ec_2025/12-b.txt')

    g = pt.grid_as_dict(lines)
    def adj(p):
        cand = pt.adj_ortho(p, g)
        return {c for c in cand if g[p] >= g[c]}
    ngh = Dictlike(adj)

    reach_tl = dijkstra(ngh, start_point=(0, 0), keep_paths=False)
    br_pt = img.max_xy(g)
    reach_br = dijkstra(ngh, start_point=br_pt, keep_paths=False)

    if output:
        def color(x, y, c):
            opt = (x, y)
            if opt in reach_tl:
                if opt in reach_br:
                    return ansi.yellow(c)
                return ansi.red(c)
            if opt in reach_br:
                return ansi.green(c)
            return c
        img.print_image(g, use_char=True, highlighter=color)

    return len(set(reach_tl).union(reach_br))

def part3(output=False):
    lines = parse('data/ec_2025/12-c.txt')

    g = pt.grid_as_dict(lines)
    exclude = set()
    def adj(p):
        cand = pt.adj_ortho(p, g)
        return {c for c in cand if c not in exclude and g[p] >= g[c]}
    ngh = Dictlike(adj)

    reached_points = {}
    for i in range(3):
        skip = set(exclude)
        max_reach = 0
        for gg in g:
            if gg in skip:
                continue
            reach = dijkstra(ngh, start_point=gg, keep_paths=False)
            reach_cnt = len(reach)
            if reach_cnt > max_reach:
                max_reach = reach_cnt
                reached_points[i] = reach
            skip = skip.union(reach)
        exclude = exclude.union(reached_points[i])

    if output:
        def color(x, y, c):
            opt = (x, y)
            if opt in reached_points[0]:
                return ansi.red(c)
            if opt in reached_points[1]:
                return ansi.green(c)
            if opt in reached_points[2]:
                return ansi.blue(c)
            return c
        img.print_image(g, use_char=True, highlighter=color)

    return len(exclude)
