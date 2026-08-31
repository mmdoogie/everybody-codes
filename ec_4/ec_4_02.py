from mrm.dijkstra import Dictlike, dijkstra
import mrm.image as img
from mrm.parse import all_nums
import mrm.point as pt

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    start = None
    moves = None
    beacons = {}
    for l in lines:
        parts = l.split('=')
        match parts[0]:
            case  'START':
                start = tuple(all_nums(parts[1]))
            case 'MOVES':
                moves = list(parts[1])
            case _:
                beacons[parts[0]] = tuple(all_nums(parts[1]))

    return start, moves, beacons

def pt_avg(pt1, pt2):
    return ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)

def part1(output=False):
    start, moves, beacons = parse('data/ec_4/02-a.txt')

    curr_pt = start
    illum = set([start])

    for m in moves:
        curr_pt = pt_avg(curr_pt, beacons[m])
        illum.add(curr_pt)
        if output:
            print(curr_pt)

    return len(illum)

def part2(output=False):
    start, moves, beacons = parse('data/ec_4/02-b.txt')

    curr_pt = start
    illum = set([start])

    for m in moves:
        curr_pt = pt_avg(curr_pt, beacons[m])
        illum.add(curr_pt)
        if output:
            print(curr_pt)

    fireflies = set()
    for i in illum:
        fireflies.update(pt.adj_ortho(i))

    return len(fireflies - illum)

def part3(output=False):
    start, _, beacons = parse('data/ec_4/02-c.txt')

    ngh = Dictlike(lambda pt: [pt_avg(pt, b) for b in beacons.values()])
    vis = dijkstra(ngh, start_point = start, keep_paths=False)

    illum = set(vis.keys())
    fireflies = set()
    for i in illum:
        fireflies.update(pt.adj_ortho(i))

    if output:
        def h(x, y, _):
            for b in beacons.items():
                if b[1] == (x, y):
                    return b[0]
            if (x, y) in illum:
                return 'X'
            if (x, y) in fireflies:
                return 'F'
            return ' '
        img.print_image(fireflies, highlighter=h)

    return len(fireflies - illum)
