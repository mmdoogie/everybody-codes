from functools import partial

from mrm.cache import Keycache
from mrm.dijkstra import Dictlike
from mrm.graph import bfs_dist
import mrm.image as img
import mrm.point as pt

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid = pt.grid_as_dict(lines)
    dragon = [gl for gl, gc in grid.items() if gc == 'D'][0]
    sheepies = {gl for gl, gc in grid.items() if gc == 'S'}
    hideouts = {gl for gl, gc in grid.items() if gc == '#'}
    return grid, dragon, sheepies, hideouts

def part1(output=False):
    grid, dragon, sheepies, _ = parse('data/ec_2025/10-a.txt')

    ngh = Dictlike(partial(pt.adj_knight, constrain_pos=grid))
    reach = bfs_dist(ngh, dragon, 4)
    all_reach = set(loc for dist in reach for loc in reach[dist])

    return sum(1 for loc in all_reach if loc in sheepies)

def part2(output=False):
    grid, dragon, sheepies, hideouts = parse('data/ec_2025/10-b.txt')
    _, max_y = img.max_xy(grid)

    ngh = Dictlike(partial(pt.adj_knight, constrain_pos=grid))
    reach = bfs_dist(ngh, dragon, 20)

    tot = 0
    sheep_pos = set(sheepies)
    for r in range(1, 21):
        # Dragon eats after dragon moves
        dragon_pos = reach[r]
        ate = {s for s in sheep_pos if s in dragon_pos and s not in hideouts}
        tot += len(ate)
        sheep_pos -= ate

        # Dragon eats after sheepies move
        sheep_pos = {(sx, sy+1) for sx, sy in sheep_pos if sy+1 <= max_y}
        ate = {s for s in sheep_pos if s in dragon_pos and s not in hideouts}
        tot += len(ate)
        sheep_pos -= ate

    return tot

def get_exits(sheepies, hideouts, max_y):
    sheep_exits = {}
    for s in sheepies:
        not_hide = s[1]
        for y in range(s[1], max_y+1):
            if (s[0], y) not in hideouts:
                not_hide = y
        sheep_exits[s[0]] = not_hide
    return sheep_exits

def part3(output=False):
    grid, dragon, sheepies, hideouts = parse('data/ec_2025/10-c.txt')
    max_x, max_y = img.max_xy(grid)
    num_cols = max_x + 1

    sheep_exits = get_exits(sheepies, hideouts, max_y)

    # state definition:
    #     dragon position
    #     sheep y positions: -1 = eaten
    #     whose turn: 1, 2 dragon first or second, -1, -2 sheep coming from dragon 1 or 2
    # ((dx, dy), (sy0, sy1, sy2, ...), dturn)

    def ngh(state):
        dragon_pos, sheep_ys, turn = state
        if turn > 2:
            return []
        next_states = []
        if turn == 1 or turn == 2:
            cand = pt.adj_knight(dragon_pos, grid)
            for c in cand:
                eaten_ys = tuple(-1 if c not in hideouts and c == s_pos else s_pos[1] for s_pos in enumerate(sheep_ys))
                next_states += [(c, eaten_ys, -turn)]
            return next_states
        had_exit = False
        for sx, sy in enumerate(sheep_ys):
            if sy == -1:
                continue
            if sy == sheep_exits[sx]:
                had_exit = True
                continue
            if dragon_pos not in hideouts and dragon_pos[0]==sx and dragon_pos[1]==sy+1:
                continue
            moved_ys = sheep_ys[:sx] + (sy+1, ) + sheep_ys[sx+1:]
            next_states += [(dragon_pos, moved_ys, 1)]
        if not next_states and not had_exit and sum(sheep_ys) != -num_cols and turn != -2:
            next_states += [(dragon_pos, sheep_ys, 2)]
        return next_states

    init_state = (dragon, tuple(-1 if (sx, 0) not in sheepies else 0 for sx in range(num_cols)), -1)

    curr_path = set()
    @Keycache(stats=True)
    def dfs(at, *, key):
        if sum(at[1]) == -num_cols:
            return 1

        curr_path.add(at)
        path_cnt = 0
        for n in ngh(at):
            if n not in curr_path:
                path_cnt += dfs(n, key=n)
        curr_path.remove(at)
        return path_cnt

    path_cnt = dfs(init_state, key=init_state)
    if output:
        hits, misses = dfs.stats()
        print(f'DFS Cache: Hits {hits} ({hits / (hits + misses) * 100:.1f}%), Misses {misses}, Total {hits + misses}')
    return path_cnt
