from itertools import cycle

import mrm.ansi_term as ansi
import mrm.point as pt

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid = pt.grid_as_dict(lines, valid=lambda x: x != '.', conv=int)
    return grid, len(lines), len(lines[0])

def part1(output=False):
    grid, height, _ = parse('data/ec_2026/08-a.txt')
    mid_row = height // 2

    energy = 0
    for start_row in range(mid_row, -mid_row - 1, -1):
        shadow = 0
        for o in range(0, height - start_row):
            loc = (mid_row - start_row + o, start_row + o)
            if loc not in grid:
                continue
            emph = False
            if grid[loc] > shadow:
                energy += 1
                shadow = grid[loc]
                emph = True
            if output:
                print(ansi.red(str(grid[loc])) if emph else grid[loc], end='-')
            shadow -= 1
        if output:
            print()

    return energy

def part2(output=False):
    grid, height, width = parse('data/ec_2026/08-b.txt')
    mid_row = height // 2

    starts  = [(0, mid_row), (width - 1, mid_row), (width - 1, 0), (width - 1, mid_row), (0, mid_row), (0, 0)]
    scans   = [(1, -1), (-1, -1), ( 0, 1), (-1,  1), (1,  1), (0, 1)]
    travels = [(1,  1), (-1,  1), (-1, 0), (-1, -1), (1, -1), (1, 0)]

    def calc_energy(start, scan, travel):
        energy = 0
        for cnt in range(height):
            shadow = 0
            head = (start[0] + scan[0] * cnt, start[1] + scan[1] * cnt)
            for off in range(width):
                at = (head[0] + travel[0] * off, head[1] + travel[1] * off)
                if at not in grid:
                    continue
                emph = False
                if grid[at] > shadow:
                    energy += 1
                    shadow = grid[at]
                    emph = True
                if output:
                    print(ansi.red(str(grid[at])) if emph else grid[at], end='-')
                shadow -= 1
            if output:
                print()
        if output:
            print()
        return energy

    energy = sum(calc_energy(st, sc, tr) for st, sc, tr in zip(starts, scans, travels))
    return energy

def part3(output=False):
    grid, height, width = parse('data/ec_2026/08-c.txt')
    mid_row = height // 2

    starts  = [(0, mid_row), (width - 1, mid_row), (width - 1, 0), (width - 1, mid_row), (0, mid_row), (0, 0)]
    scans   = [(1, -1), (-1, -1), ( 0, 1), (-1,  1), (1,  1), (0, 1)]
    travels = [(1,  1), (-1,  1), (-1, 0), (-1, -1), (1, -1), (1, 0)]

    def calc_energy(start, scan, travel):
        energy = 0
        army = 0
        for cnt in range(height):
            shadow = 0
            head = (start[0] + scan[0] * cnt, start[1] + scan[1] * cnt)
            for off in range(width):
                at = (head[0] + travel[0] * off, head[1] + travel[1] * off)
                if at not in grid:
                    continue
                if grid[at] > shadow:
                    energy += 1
                    shadow = grid[at]
                    grid[at] += 1
                    if grid[at] == 10:
                        army += 1
                        grid[at] = -4
                shadow = max(shadow - 1, 0)
        return energy, army

    tot_energy = 0
    tot_army = 0
    pat = zip(cycle(starts), cycle(scans), cycle(travels))
    cnt = 0
    while tot_army < 100000:
        st, sc, tr = next(pat)
        e, a = calc_energy(st, sc, tr)
        tot_energy += e
        tot_army += a

        for g in grid:
            if grid[g] < 0:
                grid[g] += 1
                if grid[g] == 0:
                    grid[g] = 1
        cnt += 1
        if output:
            print(f'Round: {cnt:4}, Energy: {tot_energy:6} (+{e:3}), Armies: {tot_army:6} (+{a:2})')

    return tot_energy
