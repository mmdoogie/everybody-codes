from mrm.image import print_image
from mrm.point import adj_diag, adj_ortho, grid_as_dict

def file_lines(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip() for l in f.readlines()]
    return lines

def dig_grid(grid, ngh_fun, output):
    for k, v in grid.items():
        if v == '#':
            grid[k] = 1

    lvl = 1
    tot = sum(grid[g] == lvl for g in grid)
    if output:
        print('Level', lvl, 'dug', tot, 'total', tot)
        print_image(grid, use_char=True)
        print()

    while True:
        lvl += 1
        dig = set()

        for k, v in grid.items():
            if v != lvl - 1:
                continue
            ngh = ngh_fun(k)
            if all(grid.get(n, 0) == lvl - 1 for n in ngh):
                dig.add(k)

        tot += len(dig)
        for d in dig:
            grid[d] = lvl

        if output:
            print('Level', lvl, 'dug', len(dig), 'total', tot)
            print_image(grid, use_char=True)
            print()

        if len(dig) == 0:
            break

    return tot

def part1(output):
    lines = file_lines('data/ec_2024/03-a.txt')
    grid = grid_as_dict(lines)

    return dig_grid(grid, adj_ortho, output)

def part2(output):
    lines = file_lines('data/ec_2024/03-b.txt')
    grid = grid_as_dict(lines)

    return dig_grid(grid, adj_ortho, output)

def part3(output):
    lines = file_lines('data/ec_2024/03-c.txt')
    grid = grid_as_dict(lines)

    return dig_grid(grid, adj_diag, output)
