from functools import partial

from mrm.dijkstra import Dictlike, dijkstra
from mrm.point import grid_as_dict, adj_ortho

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip() for l in f.readlines()]

    grid = grid_as_dict(lines, valid=lambda x: x not in '# ')
    neighbors = {g: adj_ortho(g, grid) for g in grid}
    weights = Dictlike(partial(move_time, grid))

    return grid, neighbors, weights

def get_level(grid, pt):
    val = grid[pt]
    if val in 'SE':
        return 0
    return int(val)

def move_time(grid, move):
    src, dest = move
    levels = abs(get_level(grid, dest) - get_level(grid, src))
    if levels > 5:
        return 10 - levels + 1
    return levels + 1

def get_matching_points(grid, label):
    return [k for k, v in grid.items() if v == label]

def part1(output):
    grid, neigh, wts = parse('data/ec_2024/13-a.txt')
    s_pt = get_matching_points(grid, 'S')[0]
    e_pt = get_matching_points(grid, 'E')[0]
    dists = dijkstra(neigh, wts, start_point=s_pt, end_point=e_pt, keep_paths=False)
    return dists[e_pt]

def part2(output):
    grid, neigh, wts = parse('data/ec_2024/13-b.txt')
    s_pt = get_matching_points(grid, 'S')[0]
    e_pt = get_matching_points(grid, 'E')[0]
    dists = dijkstra(neigh, wts, start_point=s_pt, end_point=e_pt, keep_paths=False)
    return dists[e_pt]

def part3(output):
    grid, neigh, wts = parse('data/ec_2024/13-c.txt')
    s_pts = get_matching_points(grid, 'S')
    e_pt = get_matching_points(grid, 'E')[0]
    dists = dijkstra(neigh, wts, start_point=e_pt, keep_paths=False)
    return min(dists[s] for s in s_pts)
