from functools import reduce, partial
from itertools import combinations, groupby, pairwise, product
from math import inf
import operator

import mrm.ansi_term as ansi
from mrm.dijkstra import dijkstra
from mrm.image import print_image
from mrm.point import adj_ortho, grid_as_dict
from mrm.tsp import held_karp, held_karp_dist

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip() for l in f.readlines()]
    return lines

def highlighter(path, x, y, c):
    if y == 0 and c == '.':
        return ansi.green('S')
    if c not in '.#':
        return ansi.red(c)
    if (x, y) in path:
        return ansi.yellow('*')
    if c == '.':
        return ' '
    return c

def part1(output):
    lines = parse('data/ec_2024/15-a.txt')
    grid = grid_as_dict(lines, lambda x: x not in '#')
    ngh = {g: adj_ortho(g, grid) for g in grid}

    sp = [g for g in grid if g[1] == 0][0]
    w, p = dijkstra(ngh, start_point=sp)

    h_list = [k for k, v in grid.items() if v == 'H']
    min_dist, closest_h = min((w[h], h) for h in  h_list)
    if output:
        print_image(grid, use_char=True, default_char = '#', highlighter=partial(highlighter, p[closest_h]))

    return 2 * min_dist

def reduce_graph(ngh, key_pts):
    travel_time = {}
    for src, group in groupby(combinations(key_pts, 2), lambda x: x[0]):
        wts = dijkstra(ngh, start_point=src, keep_paths=False)
        for src, dest in group:
            travel_time[(src, dest)] = wts[dest]
            travel_time[(dest, src)] = wts[dest]
    return travel_time

def part2(output):
    lines = parse('data/ec_2024/15-b.txt')
    max_x = len(lines[0]) // 2 + 8
    grid = grid_as_dict((l[:max_x] for l in lines), lambda x: x not in '#~')
    ngh = {g: adj_ortho(g, grid) for g in grid}

    herbs = set(grid.values()).difference(['.'])
    herb_points = {h: [k for k, v in grid.items() if v==h] for h in herbs}
    sp = [g for g in grid if g[1] == 0][0]

    key_pts = reduce(operator.add, herb_points.values()) + [sp]
    travel_time = reduce_graph(ngh, key_pts)

    min_hd = inf
    min_picks = None
    for picks in product([sp], *herb_points.values()):
        hd = held_karp_dist(picks, travel_time, start_point=sp, max_dist=min_hd)
        if hd and hd < min_hd:
            min_hd = hd
            min_picks = picks

    if output:
        hd, hr = held_karp(min_picks, travel_time, start_point=sp)
        cons = []
        for a, b in pairwise(hr):
            _, p = dijkstra(ngh, start_point=a, end_point=b)
            cons += p[b]

        print_image(grid, use_char=True, default_char='#', highlighter=partial(highlighter, cons))

    return min_hd

def tsp_section(travel_time, fixed_pts, search_pts, start_point):
    min_dist = inf
    min_path = None
    for picks in product(*search_pts):
        tsp_pts = list(picks) + fixed_pts
        dist, path = held_karp(tsp_pts, travel_time, start_point=start_point)
        if dist < min_dist:
            min_dist = dist
            min_path = path
    return min_dist, min_path

def left_half(points_list):
    min_x = min(p[0] for p in points_list)
    return [p for p in points_list if p[0] == min_x]

def part3(output):
    lines = parse('data/ec_2024/15-c.txt')
    grid = grid_as_dict(lines, lambda x: x not in '#~')
    ngh = {g: adj_ortho(g, grid) for g in grid}

    herbs = set(grid.values()).difference(['.'])
    herb_points = {h: [k for k,v in grid.items() if v==h] for h in herbs}
    for h in herb_points:
        if h not in 'AGNCIP':
            continue
        herb_points[h] = left_half(herb_points[h])
    sp = [g for g in grid if g[1] == 0][0]

    key_pts = reduce(operator.add, herb_points.values()) + [sp]
    travel_time = reduce_graph(ngh, key_pts)

    # Left Section: find the interior E and the closest A
    # Assume all paths hit one of the B to reduce computation
    loc_e = herb_points['E'][1]
    loc_a = min((travel_time[(loc_e, cand)], cand) for cand in herb_points['A'])[1]
    left_dist, left_path = tsp_section(travel_time, [loc_e, loc_a], [v for k, v in herb_points.items() if k in 'CD'], loc_e)

    # Right Section: interior R to closest N, assume O covered
    loc_r = herb_points['R'][0]
    loc_n = min((travel_time[(loc_r, cand)], cand) for cand in herb_points['N'])[1]
    right_dist, right_path = tsp_section(travel_time, [loc_r, loc_n], [v for k, v in herb_points.items() if k in 'PQ'], loc_r)
    # O not covered?

    # Center Section: pick a closest G to use, assume H covered
    # Have to hit E and R to link adjacent sections
    loc_g = min((travel_time[(sp, cand)], cand) for cand in herb_points['G'])[1]
    center_dist, center_path = tsp_section(travel_time, [sp, loc_g, loc_e, loc_r], [v for k, v in herb_points.items() if k in 'IJ'], sp)

    if output:
        cons = []
        for path in [left_path, right_path, center_path]:
            for a, b in pairwise(path):
                _, p = dijkstra(ngh, start_point=a, end_point=b)
                cons += p[b]

        print_image(grid, use_char=True, default_char = '#', highlighter=partial(highlighter, cons))

    return center_dist + left_dist + right_dist
