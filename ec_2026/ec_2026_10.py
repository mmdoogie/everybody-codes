from collections import Counter

import mrm.cpoint as cpt

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid = cpt.grid_as_dict(lines)
    dirs = {'>': cpt.RIGHT, '<': cpt.LEFT, '^': cpt.UP, 'v': cpt.DOWN}
    ghosts = {e: (k, dirs[v]) for e, (k, v) in enumerate(grid.items()) if v in ''.join(dirs)}
    walls = set(k for k, v in grid.items() if v == '#')
    return ghosts, walls

def part1(output=False):
    ghosts, walls = parse('data/ec_2026/10-a.txt')

    collisions = 0
    for _ in range(10):
        for g in ghosts:
            loc, head = ghosts[g]
            next_loc = cpt.go_dist(loc, head, 1)
            if next_loc in walls:
                head = cpt.right_turn(head)
                next_loc = loc
                collisions += 1
            ghosts[g] = (next_loc, head)
        ghosts_at_loc = Counter(l for l, _ in ghosts.values())
        for g in ghosts:
            loc, head = ghosts[g]
            if ghosts_at_loc[loc] > 1:
                ghosts[g] = (loc, cpt.u_turn(head))
                collisions += 1

    return collisions

def part2(output=False):
    ghosts, walls = parse('data/ec_2026/10-b.txt')
    collisions = {g: 0 for g in ghosts}

    rounds = 0
    to_rem = set()
    while ghosts:
        to_rem.clear()
        for g in ghosts:
            loc, head = ghosts[g]
            next_loc = cpt.go_dist(loc, head, 1)
            if next_loc in walls:
                head = cpt.right_turn(head)
                next_loc = loc
                collisions[g] += 1
                if collisions[g] == 10000:
                    to_rem.add(g)
            ghosts[g] = (next_loc, head)
        for g in to_rem:
            del ghosts[g]
        ghosts_at_loc = Counter(l for l, _ in ghosts.values())
        to_rem.clear()
        for g in ghosts:
            loc, head = ghosts[g]
            if ghosts_at_loc[loc] > 1:
                ghosts[g] = (loc, cpt.u_turn(head))
                collisions[g] += 1
                if collisions[g] == 10000:
                    to_rem.add(g)
        for g in to_rem:
            del ghosts[g]
        rounds += 1

    return rounds

def part3(output=False):
    ghosts, walls = parse('data/ec_2026/10-c.txt')
    collisions = {g: 0 for g in ghosts}
    max_collisions = 1000000000000

    def cfg_hash():
        return tuple(ghosts.items())

    rounds = 0
    h = cfg_hash()
    seen = {h: 0}
    seen_collisions = {h: dict(collisions.items())}
    to_rem = set()
    while ghosts:
        rounds += 1
        to_rem.clear()
        for g in ghosts:
            loc, head = ghosts[g]
            next_loc = cpt.go_dist(loc, head, 1)
            if next_loc in walls:
                head = cpt.right_turn(head)
                next_loc = loc
                collisions[g] += 1
                if collisions[g] == max_collisions:
                    to_rem.add(g)
            ghosts[g] = (next_loc, head)
        for g in to_rem:
            del ghosts[g]
            del collisions[g]
        if to_rem:
            if output:
                print(f'At round {rounds}, {len(ghosts)} remain')
            seen.clear()
            seen_collisions.clear()
            to_rem.clear()
        ghosts_at_loc = Counter(l for l, _ in ghosts.values())
        for g in ghosts:
            loc, head = ghosts[g]
            if ghosts_at_loc[loc] > 1:
                ghosts[g] = (loc, cpt.u_turn(head))
                collisions[g] += 1
                if collisions[g] == max_collisions:
                    to_rem.add(g)
        for g in to_rem:
            del ghosts[g]
            del collisions[g]
        if to_rem:
            if output:
                print(f'At round {rounds}, {len(ghosts)} remain')
            seen.clear()
            seen_collisions.clear()

        h = cfg_hash()
        if h in seen:
            if output:
                print(f'Cfg Loop Detected from {seen[h]} to {rounds}')
            deltas = {g: collisions[g] - seen_collisions[h][g] for g in ghosts}

            max_g = max(collisions.items(), key=lambda x: x[1])[0]
            offset = seen_collisions[h][max_g]
            multip = (max_collisions - offset) // deltas[max_g]
            if len(ghosts) == 1:
                g = list(ghosts.keys())[0]
                if seen_collisions[h][g] + multip * deltas[g] == max_collisions:
                    multip -= 1
            ff_round = seen[h] + multip * (rounds - seen[h])
            to_rem.clear()
            for g in ghosts:
                loc, head = ghosts[g]
                ff_collisions = seen_collisions[h][g] + multip * deltas[g]
                if ff_collisions < max_collisions:
                    collisions[g] = ff_collisions
                else:
                    to_rem.add(g)
            for g in to_rem:
                del ghosts[g]
                del collisions[g]
            rounds = ff_round
            if output:
                print(f'FF to {rounds} ({multip}x)')
                if to_rem:
                    print(f'At round {rounds}, {len(ghosts)} remain')
            seen.clear()
            seen_collisions.clear()
            continue

        seen[h] = rounds
        seen_collisions[h] = dict(collisions.items())

    return rounds
