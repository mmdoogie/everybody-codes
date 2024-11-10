from collections import defaultdict
from mrm.llist import llist

def read_grid(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip() for l in f.readlines()]
    grid = [[int(v) for v in l.split(' ')] for l in lines]
    cols = [llist(grid[r][c] for r in range(len(grid))) for c in range(4)]
    return cols

def do_round(cols, r):
    col = r % 4
    clapper = cols[col].head().val
    cols[col].drop(cols[col].head())
    col = (r + 1) % 4
    colmax = len(cols[col]) - 1
    near = -1
    side = 1
    for c in range(clapper):
        if (near == colmax and side == 1) or (near == 0 and side == -1):
            side = -side
            continue
        near += side
    if side == 1:
        cols[col].insert_left_of(cols[col].head().far_right(near), clapper)
    else:
        cols[col].insert_right_of(cols[col].head().far_right(near), clapper)
    return int(''.join(str(c.head().val) for c in cols))

def part1(output):
    cols = read_grid('data/ec_2024/05-a.txt')
    for r in range(10):
        shout = do_round(cols, r)
    return shout

def part2(output):
    cols = read_grid('data/ec_2024/05-b.txt')
    shout_cnt = defaultdict(int)
    r = 0
    while True:
        shout = do_round(cols, r)
        c = shout_cnt[shout] + 1
        shout_cnt[shout] = c
        r += 1
        if c == 2024:
            return r * shout

def part3(output):
    cols = read_grid('data/ec_2024/05-c.txt')
    r = 0
    max_shout = 0
    seen = set()
    while True:
        shout = do_round(cols, r)
        max_shout = max(max_shout, shout)
        state = ''.join(str(v.val) for c in cols for v in c)
        if state in seen:
            break
        seen.add(state)
        r += 1
    return max_shout
