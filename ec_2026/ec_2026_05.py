import mrm.ansi_term as ansi
import mrm.image as img
import mrm.point as pt

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    mid_x = (len(lines[0]) - 1) // 2
    mid_y = (len(lines) - 1) // 2
    grid = pt.grid_as_dict(lines)
    grid[(mid_x, mid_y)] = '#'
    return grid

def grid_set(grid, ch):
    return {g for g in grid if grid[g] == ch}

LIGHT = '0'
DARK  = '1'
LAND  = '#'
SAND  = '='
TREE  = '@'

IMG_COLOR = { LIGHT: ansi.blue('.'),
              DARK:  ansi.blue('.'),
              LAND:  ansi.red(LAND),
              SAND:  ansi.yellow(SAND),
              TREE:  ansi.green(TREE) }
def imgcolor(_x, _y, c):
    if c in IMG_COLOR:
        return IMG_COLOR[c]
    return c

def part1(output=False):
    grid = parse('data/ec_2026/05-a.txt')

    land = grid_set(grid, LAND)
    while True:
        expand = set()
        for at_land in land:
            for adj_pt in pt.adj_diag(at_land, grid):
                if grid[adj_pt] == LAND:
                    continue
                num_dark = sum(1 for p in pt.adj_diag(adj_pt, grid) if grid[p] != LIGHT)
                if num_dark >= 5:
                    expand.add(adj_pt)
        if not expand:
            break
        for e in expand:
            grid[e] = LAND
        land |= expand

    if output:
        img.print_image(grid, use_char=True, highlighter=imgcolor)

    return len(land)

def part2(output=False):
    grid = parse('data/ec_2026/05-b.txt')
    land = grid_set(grid, LAND)
    while True:
        expand = set()
        for at_land in land:
            for adj_pt in pt.adj_diag(at_land, grid):
                if grid[adj_pt] == LAND:
                    continue
                num_dark = sum(1 for p in pt.adj_diag(adj_pt, grid) if grid[p] != LIGHT)
                if num_dark >= 5:
                    expand.add(adj_pt)
        if not expand:
            break
        for e in expand:
            grid[e] = LAND
        land |= expand

    expand = set()
    for at_land in land:
        if any(p not in grid or grid[p] != LAND for p in pt.adj_diag(at_land)):
            expand.add(at_land)
    for e in expand:
        grid[e] = SAND
    land |= expand

    while True:
        expand = set()
        for at_land in land:
            num_sand = sum(1 for p in pt.adj_diag(at_land, grid) if grid[p] == SAND)
            if num_sand >= 5:
                expand.add(at_land)
        if not expand:
            break
        for e in expand:
            grid[e] = SAND
        land ^= expand

    if output:
        img.print_image(grid, use_char=True, highlighter=imgcolor)

    return len(grid_set(grid, SAND))

BASE_KERN = { (dx, dy) for dx in range(-2, 3) for dy in range(-2, 3)
              if (dx, dy) not in [(-2, -2), (2, -2), (-2, 2), (2, 2), (0, 0)] }
def adj_kern(p, grid):
    adj = {(p[0] + b[0], p[1] + b[1]) for b in BASE_KERN}
    return {a for a in adj if a in grid}

def part3(output=False):
    grid = parse('data/ec_2026/05-c.txt')
    land = grid_set(grid, LAND)
    while True:
        expand = set()
        for at_land in land:
            for adj_pt in pt.adj_diag(at_land, grid):
                if grid[adj_pt] == LAND:
                    continue
                num_dark = sum(1 for p in pt.adj_diag(adj_pt, grid) if grid[p] != LIGHT)
                if num_dark >= 5:
                    expand.add(adj_pt)
        if not expand:
            break
        for e in expand:
            grid[e] = LAND
        land |= expand

    expand = set()
    for at_land in land:
        if any(p not in grid or grid[p] != LAND for p in pt.adj_diag(at_land)):
            expand.add(at_land)
    for e in expand:
        grid[e] = SAND
    land |= expand

    while True:
        expand = set()
        for at_land in land:
            num_sand = sum(1 for p in pt.adj_diag(at_land, grid) if grid[p] == SAND)
            if num_sand >= 5:
                expand.add(at_land)
        if not expand:
            break
        for e in expand:
            grid[e] = SAND
        land ^= expand

    for at_land in land:
        expand = set()
        if all(grid[p] in '#@' for p in adj_kern(at_land, grid)):
            grid[at_land] = '@'
            expand.add(at_land)
    land ^= expand

    for _ in range(2):
        expand = set()
        for at_land in land:
            if sum(1 for p in pt.adj_diag(at_land, grid) if grid[p] == TREE) >= 4 \
               and all(grid[p] != SAND for p in pt.adj_diag(at_land, grid)):
                expand.add(at_land)
        for e in expand:
            grid[e] = TREE
    land ^= expand

    if output:
        img.print_image(grid, use_char=True, highlighter=imgcolor)

    return len(grid_set(grid, TREE))
