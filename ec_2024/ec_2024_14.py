from mrm.dijkstra import dijkstra
import mrm.point as pt

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip() for l in f.readlines()]
    return lines

def part1(output):
    lines = parse('data/ec_2024/14-a.txt')
    instr = lines[0].split(',')
    z = 0
    max_z = 0
    mult = {'U': 1, 'D': -1}
    for i in instr:
        z += mult.get(i[0], 0) * int(i[1:])
        if z > max_z:
            max_z = z
    return max_z

def part2(output):
    lines = parse('data/ec_2024/14-b.txt')
    dists = {'R': (1, 0, 0), 'L': (-1,  0,  0),
             'F': (0, 1, 0), 'B': ( 0, -1,  0),
             'U': (0, 0, 1), 'D': ( 0,  0, -1)}

    points = set()
    for l in lines:
        instr = l.split(',')
        curr_pt = pt.ZERO_3D
        for i in instr:
            incr = dists[i[0]]
            for _ in range(int(i[1:])):
                curr_pt = pt.point_add(curr_pt, incr)
                points.add(curr_pt)
    return len(points)

def part3(output):
    lines = parse('data/ec_2024/14-c.txt')
    dists = {'R': (1, 0, 0), 'L': (-1,  0,  0),
             'F': (0, 1, 0), 'B': ( 0, -1,  0),
             'U': (0, 0, 1), 'D': ( 0,  0, -1)}

    points = set()
    leaves = set()
    for l in lines:
        instr = l.split(',')
        curr_pt = pt.ZERO_3D
        for i in instr:
            incr = dists[i[0]]
            for _ in range(int(i[1:])):
                curr_pt = pt.point_add(curr_pt, incr)
                points.add(curr_pt)
        leaves.add(curr_pt)

    ngh = {p: pt.adj_ortho(p, points) for p in points}
    all_wts = {}
    for l in leaves:
        wts = dijkstra(ngh, start_point=l, keep_paths=False)
        all_wts[l] = wts

    if output:
        print('Segments:', len(points))
        print('Leaves  :', len(leaves))

    return min(sum(all_wts[l][p] for l in leaves) for p in points)
