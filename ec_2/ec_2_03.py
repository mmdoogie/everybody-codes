from mrm.dijkstra import dijkstra, Dictlike
from mrm.parse import all_nums
import mrm.point as pt

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

class RollerDie:
    def __init__(self, faces, seed):
        self.faces = faces
        self.seed = seed
        self.pulse = seed
        self.rolls = 0
        self.curr = 0
        self.spin = 0

    def reset(self):
        self.pulse = self.seed
        self.rolls = 0
        self.curr = 0
        self.spin = 0

    def __next__(self):
        self.rolls += 1
        self.spin = self.rolls * self.pulse
        self.pulse = ((self.pulse + self.spin) % self.seed) + 1 + self.rolls + self.seed
        self.curr = (self.curr + self.spin) % len(self.faces)
        return self.faces[self.curr]

def dice_from(lines):
    nums = [list(all_nums(l))[1:] for l in lines]
    return [RollerDie(n[:-1], n[-1]) for n in nums]

def part1(output=False):
    lines = parse('data/ec_2/03-a.txt')
    dice = dice_from(lines)

    tot = 0
    while tot < 10000:
        for d in dice:
            tot += next(d)

    return dice[0].rolls

def part2(output=False):
    lines = parse('data/ec_2/03-b.txt')
    dice = dice_from(lines[:-2])
    track = [int(x) for x in lines[-1]]

    rolls = {}
    for dn, d in enumerate(dice):
        die_track = iter(track)
        spot = next(die_track)

        for spot in die_track:
            roll = next(d)
            while roll != spot:
                roll = next(d)

        rolls[dn] = d.rolls

    return ','.join([f'{dn + 1}' for dn, _ in sorted(rolls.items(), key=lambda i: i[1])])

def part3(output=False):
    lines = parse('data/ec_2/03-c.txt')
    dice = dice_from(lines[:9])
    grid = {k: int(v) for k, v in pt.grid_as_dict(lines[10:]).items()}

    pool_coins = set()
    for d in dice:
        rolls = {n: next(d) for n in range(5000)}

        def adj(loc):
            x, y, rn = loc
            poss = [(x, y)] + pt.adj_ortho((x, y), grid)
            return [(*xy, rn + 1) for xy in poss if grid[xy] == rolls[rn + 1]]

        starts = [gk for gk, gv in grid.items() if gv == rolls[0]]
        for s in starts:
            wts = dijkstra(Dictlike(adj), start_point=(*s, 0), keep_paths=False)
            coins_from = set((x, y) for x, y, _ in wts)
            pool_coins |= coins_from

    return len(pool_coins)
