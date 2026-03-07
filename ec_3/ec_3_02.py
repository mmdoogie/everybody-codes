from itertools import cycle, repeat, chain

import mrm.cpoint as cpt

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    _, inv = cpt.grid_as_dict(lines, with_inv=True)
    return inv

MV_PAT = [cpt.UP, cpt.RIGHT, cpt.DOWN, cpt.LEFT]
LONG_MV_PAT = list(chain.from_iterable(repeat(x, 3) for x in MV_PAT))

def part1(output=False):
    inv = parse('data/ec_3/02-a.txt')

    at = inv['@'].pop()
    end = inv['#'].pop()

    visited = set([at])
    for p in cycle(MV_PAT):
        if at + p in visited:
            continue
        at = at + p
        visited.add(at)
        if at == end:
            break

    return len(visited) - 1

def part2(output=False):
    inv = parse('data/ec_3/02-b.txt')

    at = inv['@'].pop()
    end = inv['#'].pop()

    visited = set([at, end])
    for p in cycle(MV_PAT):
        if at + p in visited:
            continue
        at = at + p
        visited.add(at)
        if all(end + m in visited for m in MV_PAT):
            break

    return len(visited) - 2

def try_flood(visited, loc):
    chk_from = set([loc])
    while True:
        add = set()
        for pt in chk_from:
            add.update(adj for adj in cpt.adj_ortho(pt) if adj not in chk_from and adj not in visited)
        if not add:
            break
        chk_from |= add
        if len(chk_from) > 100:
            return set()
    visited |= chk_from
    return chk_from

def part3(output=False):
    inv = parse('data/ec_3/02-c.txt')

    at = inv['@'].pop()
    end = inv['#']

    visited = set([at]) | end
    remain = set(a for e in end for a in cpt.adj_ortho(e))
    remain -= end

    ini_flood=set()
    for r in remain:
        if r in visited:
            continue
        ini_flood |= try_flood(visited, r)
    remain -= ini_flood

    moves = 0
    for p in cycle(LONG_MV_PAT):
        if at + p in visited:
            continue

        moves += 1
        at = at + p

        visited.add(at)
        remain.discard(at)
        if not remain:
            break

        for loc in cpt.adj_ortho(at):
            if loc in visited:
                continue
            remain -= try_flood(visited, loc)
        if not remain:
            break

    return moves
