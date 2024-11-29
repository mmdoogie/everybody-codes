from itertools import cycle

from mrm.bitvector import Bitvector
from mrm.image import print_image
from mrm.point import adj_diag, grid_as_dict

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    key = lines[0]
    grid = grid_as_dict(lines[2:])

    return key, grid

REORDERS = {'L': [1, 2, 4, 0, 7, 3, 5, 6],
            'R': [3, 0, 1, 5, 2, 6, 7, 4]}

def rot(grid, pos, direction):
    adj = adj_diag(pos)
    iv = [grid[a] for a in adj]

    for i in range(8):
        grid[adj[REORDERS[direction][i]]] = iv[i]

def part1(output):
    key, grid = parse('data/ec_2024/19-a.txt')

    rot_pts = [g for g in grid if len(adj_diag(g, grid)) == 8]

    kv = cycle(key)
    for r in rot_pts:
        rot(grid, r, next(kv))

    if output:
        print_image(grid, use_char=True)

    answer_pts = sorted((k, v) for k,v in grid.items() if v in '123456789')
    return ''.join([a[1] for a in answer_pts])

def compute_final(grid, key, num_rounds, output):
    rot_pts = [g for g in grid if len(adj_diag(g, grid)) == 8]

    rounds = Bitvector(iv=num_rounds)
    steps = max(rounds.bits()) + 1

    if output:
        print(f'{rounds.as_int()} rounds is {bin(rounds.as_int())} requiring 1 rotation and {steps - 1} compositions')

    mapping = {g: g for g in grid}
    kv = cycle(key)
    for r in rot_pts:
        rot(mapping, r, next(kv))

    if output:
        print('First round built')

    all_maps = [mapping]
    for n in range(1, steps):
        mapping = {k: mapping[v] for k, v in mapping.items()}
        all_maps += [mapping]
        if output:
            print(f'2^{n} = {2**n} composed')

    if output:
        print('Applying bits', rounds.bits())

    mapping = {g: g for g in grid}
    for b in rounds.bits():
        mapping = {k: all_maps[b][v] for k, v in mapping.items()}
        if output:
            print(f'2^{b} = {2**b} applied')

    if output:
        disp_grid = {k: grid[v] for k, v in mapping.items()}
        print_image(disp_grid, use_char=True)

    answer_pts = sorted((k, grid[v]) for k, v in mapping.items() if grid[v] in '123456789')
    return ''.join([a[1] for a in answer_pts])

def part2(output):
    key, grid = parse('data/ec_2024/19-b.txt')
    return compute_final(grid, key, 100, output)

def part3(output):
    key, grid = parse('data/ec_2024/19-c.txt')
    return compute_final(grid, key, 1048576000, output)
