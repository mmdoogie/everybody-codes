import math

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return [int(x) for x in lines[0].split(',')]

def part1(output=False):
    cones = parse('data/ec_2026/01-a.txt')
    need = 0
    for c in cones:
        closest_sq = math.ceil(math.sqrt(c)) ** 2
        need += closest_sq - c
    return need

def part2(output=False):
    cones = parse('data/ec_2026/01-b.txt')
    need = 0
    for c in cones:
        closest_patch = math.ceil((c - 4) / 4 + 2)
        if closest_patch <= 2:
            closest_patch = 3
        full_patch = 4 * (closest_patch - 2) + 4
        need += full_patch - c
    return need

def part3(output=False):
    cones = parse('data/ec_2026/01-c.txt')
    need = 0
    for c in cones:
        closest_patch = math.ceil(math.sqrt(c + 1))
        if closest_patch % 2 == 0:
            closest_patch += 1
        full_patch = closest_patch ** 2 - 1
        need += full_patch - c
    return need
