from mrm.dijkstra import dijkstra
from mrm.point import grid_as_dict, adj_ortho

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid = grid_as_dict(lines, valid=lambda x: x in 'P.')
    palms = {k for k, v in grid.items() if v == 'P'}
    starts = [k for k in grid if k[0] == 0 or k[0] == len(lines[0]) - 1]
    return grid, palms, starts

def part1(output):
    grid, palms, starts = parse('data/ec_2024/18-a.txt')
    ngh = {loc: adj_ortho(loc, grid) for loc in grid}
    dist = dijkstra(ngh, start_point=starts[0], keep_paths=False)
    return max(dist[p] for p in palms)

def part2(output):
    grid, palms, starts = parse('data/ec_2024/18-b.txt')
    ngh = {loc: adj_ortho(loc, grid) for loc in grid}
    dist1 = dijkstra(ngh, start_point=starts[0], keep_paths=False)
    dist2 = dijkstra(ngh, start_point=starts[1], keep_paths=False)
    return max(min(dist1[p], dist2[p]) for p in palms)

def part3(output):
    grid, palms, starts = parse('data/ec_2024/18-c.txt')
    ngh = {loc: adj_ortho(loc, grid) for loc in grid}
    palm_dist = {p: dijkstra(ngh, start_point=p, keep_paths=False) for p in palms}
    notpalms = set(grid) - palms
    return min(sum(palm_dist[p][np] for p in palms) for np in notpalms)
