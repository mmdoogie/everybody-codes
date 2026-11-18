from collections import defaultdict
from enum import Enum
from functools import partial

import mrm.ansi_term as ansi
from mrm.dijkstra import Dictlike, dijkstra
import mrm.image as img
import mrm.point as pt

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse('data/ec_2026/17-a.txt')
    grid = pt.grid_as_dict(lines, lambda x: x == '#')

    start_pt = img.min_xy(grid)
    end_pt = img.max_xy(grid)
    ngh = Dictlike(partial(pt.adj_ortho, constrain_pos=grid))

    w, p = dijkstra(ngh, start_point=start_pt, end_point=end_pt, keep_paths=True)

    if output:
        def img_chr(x, y, _):
            if (x, y) not in grid:
                return '.'
            if (x, y) in p[end_pt]:
                return ansi.red('#')
            return '#'
        img.print_image(grid, use_char=True, highlighter=img_chr, margin=0)

    return w[end_pt]

class Dir(Enum):
    HORIZ = True
    VERT = False

def make_subgrid(grid, width, height):
    subgrid = {}
    ngh = defaultdict(set)

    for y in range(height + 1):
        for x in range(width + 1):
            if ((x, y) in grid) != ((x, y - 1) in grid):
                subgrid[(x, y, Dir.HORIZ)] = '-'
                if (x - 1, y, Dir.HORIZ) in subgrid:
                    ngh[(x, y, Dir.HORIZ)].add((x - 1, y, Dir.HORIZ))
                    ngh[(x - 1, y, Dir.HORIZ)].add((x, y, Dir.HORIZ))

            if ((x - 1, y) in grid) != ((x, y) in grid):
                subgrid[(x, y, Dir.VERT)] = '|'
                if (x, y - 1, Dir.VERT) in subgrid:
                    ngh[(x, y, Dir.VERT)].add((x, y - 1, Dir.VERT))
                    ngh[(x, y - 1, Dir.VERT)].add((x, y, Dir.VERT))

    for y in range(height + 1):
        for x in range(width + 1):
            corners = [[(x,     y, Dir.HORIZ), (x,     y,     Dir.VERT)],
                       [(x,     y, Dir.HORIZ), (x + 1, y,     Dir.VERT)],
                       [(x,     y, Dir.VERT),  (x,     y + 1, Dir.HORIZ)],
                       [(x + 1, y, Dir.VERT),  (x,     y + 1, Dir.HORIZ)]]

            excludes = [(x - 1, y,     Dir.HORIZ),
                        (x + 1, y,     Dir.HORIZ),
                        (x - 1, y + 1, Dir.HORIZ),
                        (x + 1, y + 1, Dir.HORIZ)]

            for (c1, c2), ex in zip(corners, excludes):
                if (c1 in subgrid) and (c2 in subgrid) and (ex not in subgrid):
                    ngh[c1].add(c2)
                    ngh[c2].add(c1)

    ngh[(0, 0, Dir.VERT)].remove((0, 0, Dir.HORIZ))
    return ngh

def part2(output=False):
    lines = parse('data/ec_2026/17-b.txt')
    grid = pt.grid_as_dict(lines, lambda x: x == '#')
    ngh = make_subgrid(grid, len(lines[0]), len(lines))

    w = dijkstra(ngh, start_point=(0, 0, Dir.VERT), end_point=(0, 0, Dir.HORIZ), keep_paths=False)

    return w[(0, 0, Dir.HORIZ)] + 1

def part3(output=False):
    lines = parse('data/ec_2026/17-c.txt')
    grid = pt.grid_as_dict(lines, lambda x: x == '#')
    ngh = make_subgrid(grid, len(lines[0]), len(lines))

    far_pt = img.max_xy(grid)
    end_pts = [(far_pt[0], far_pt[1] + 1, Dir.HORIZ), (far_pt[0] + 1, far_pt[1], Dir.VERT)]

    w = dijkstra(ngh, start_point=(0, 0, Dir.VERT), end_point=end_pts, keep_paths=False)
    path_one = [w[e] + 1 for e in end_pts if e in w]

    w = dijkstra(ngh, start_point=(0, 0, Dir.HORIZ), end_point=end_pts, keep_paths=False)
    path_two = [w[e] + 1 for e in end_pts if e in w]

    if output:
        print('Down: ', path_one)
        print('Right:', path_two)

    return min(path_one + path_two)
