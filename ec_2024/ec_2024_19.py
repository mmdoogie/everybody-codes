from itertools import cycle
from time import sleep

import mrm.ansi_term as ansi
from mrm.image import print_image
from mrm.point import adj_diag, grid_as_dict


def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

LEFT = [1, 2, 4, 0, 7, 3, 5, 6]
RIGHT = [3, 0, 1, 5, 2, 6, 7, 4]
DIRS = {'L': LEFT, 'R': RIGHT}

def rot(grid, pos, direction):
    adj = adj_diag(pos)
    iv = [grid[a] for a in adj]

    for i in range(8):
        grid[adj[DIRS[direction][i]]] = iv[i]

def part1(output):
    lines = parse('data/ec_2024/19-a.txt')

    key = lines[0]
    grid = grid_as_dict(lines[2:])
    rot_pts = [g for g in grid if len(adj_diag(g, grid)) == 8]

    kv = cycle(key)
    for r in rot_pts:
        rot(grid, r, next(kv))

    if output:
        print_image(grid, use_char=True)

    answer_pts = sorted((k, v) for k,v in grid.items() if v in '123456789')
    return ''.join([a[1] for a in answer_pts])

def part2(output):
    lines = parse('data/ec_2024/19-b.txt')

    key = lines[0]
    grid = grid_as_dict(lines[2:])
    rot_pts = [g for g in grid if len(adj_diag(g, grid)) == 8]

    if output:
        ansi.clear_screen()

    for n in range(100):
        kv = cycle(key)
        for r in rot_pts:
            rot(grid, r, next(kv))

        if output:
            with ansi.hidden_cursor():
                ansi.cursor_home()
                print('Round', n + 1)
                print_image(grid, use_char=True)
                sleep(0.1)

    answer_pts = sorted((k, v) for k,v in grid.items() if v in '123456789')
    return ''.join([a[1] for a in answer_pts])

def part3(output):
    lines = parse('data/ec_2024/19-c.txt')

    key = lines[0]
    grid = grid_as_dict(lines[2:])
    rot_pts = [g for g in grid if len(adj_diag(g, grid)) == 8]

    mapping = {g: g for g in grid}

    for _ in range(100):
        kv = cycle(key)
        for r in rot_pts:
            rot(mapping, r, next(kv))

    rev_mapping = {v: k for k, v in mapping.items()}

    key_pts   = [k for k, v in grid.items() if v in '123456789']
    key_vals  = [v for k, v in grid.items() if v in '123456789']

    its = 1048576000 // 100
    for n in range(its):
        new_key_pts = [rev_mapping[k] for k in key_pts]
        key_pts = new_key_pts
        if output and n % 100000 == 0:
            print(f'Round {n:>12d}, {n / its * 100:6.2f}%')

    answer_pts = sorted((k, v) for k, v in zip(key_pts, key_vals))
    return ''.join([a[1] for a in answer_pts])
