from functools import partial

import mrm.ansi_term as ansi
from mrm.dijkstra import Dictlike, dijkstra
import mrm.cpoint as cpt
import mrm.image as img

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    instrs = lines[0].split(',')
    return [(i[0], int(i[1:])) for i in instrs]

def part1(output=False):
    instrs = parse('data/ec_2025/15-a.txt')

    at = cpt.ZERO
    face = cpt.UP
    walls = set([at])
    for i in instrs:
        if i[0] == 'L':
            face = cpt.left_turn(face)
        else:
            face = cpt.right_turn(face)

        for _ in range(i[1]):
            at = at + face
            walls.add(at)

    ngh = Dictlike(lambda p: [a for a in cpt.adj_ortho(p) if a==at or a not in walls])
    wts, paths = dijkstra(ngh, start_point=cpt.ZERO, end_point=at, dist_est=partial(cpt.m_dist, at))

    if output:
        def char_at(x, y, _):
            p = cpt.from_xy(x, y)
            if p == cpt.ZERO:
                return ansi.red('S')
            if p == at:
                return ansi.red('E')
            if p in walls:
                return '#'
            if p in paths[at]:
                return ansi.green('x')
            return ' '
        img.print_image({w: '' for w in walls}, use_char=True, highlighter=char_at)

    return wts[at]

def part2(output=False):
    instrs = parse('data/ec_2025/15-b.txt')

    at = cpt.ZERO
    face = cpt.UP
    walls = set([at])
    for i in instrs:
        if i[0] == 'L':
            face = cpt.left_turn(face)
        else:
            face = cpt.right_turn(face)

        for _ in range(i[1]):
            at = at + face
            walls.add(at)

    ngh = Dictlike(lambda p: [a for a in cpt.adj_ortho(p) if a==at or a not in walls])
    wts = dijkstra(ngh, start_point=cpt.ZERO, end_point=at, dist_est=partial(cpt.m_dist, at), keep_paths=False)

    return wts[at]

def make_segs(instrs):
    at = cpt.ZERO
    face = None

    h_segs = {}
    v_segs = {}
    for i in instrs:
        if i[0] == 'L':
            if face is None:
                face = cpt.LEFT
            else:
                face = cpt.left_turn(face)
        else:
            if face is None:
                face = cpt.RIGHT
            else:
                face = cpt.right_turn(face)

        dst = cpt.go_dist(at, face, i[1])

        if face in [cpt.LEFT, cpt.RIGHT]:
            assert cpt.y(at) not in h_segs
            x1 = cpt.x(at)
            x2 = cpt.x(dst)
            h_segs[cpt.y(at)] = range(min(x1, x2), max(x1, x2) + 1)
        else:
            assert cpt.x(at) not in v_segs
            y1 = cpt.y(at)
            y2 = cpt.y(dst)
            v_segs[cpt.x(at)] = range(min(y1, y2), max(y1, y2) + 1)

        at = dst

    return h_segs, v_segs, at

def find_moves(h_segs, hk, r_hk, v_segs, vk, r_vk, ep, at):
    ax, ay = cpt.as_xy(at, int)
    collect = set()

    for vx in vk:
        if vx < ax:
            continue
        npt = cpt.from_xy(vx - 1, ay)
        if npt != at:
            collect.add(npt)
        if ay in v_segs[vx]:
            break
        npt = cpt.from_xy(vx + 1, ay)
        collect.add(npt)
    if ax <= cpt.x(ep) <= vx:
        collect.add(cpt.from_xy(cpt.x(ep), ay))

    for vx in r_vk:
        if vx > ax:
            continue
        npt = cpt.from_xy(vx + 1, ay)
        if npt != at:
            collect.add(npt)
        if ay in v_segs[vx]:
            break
        npt = cpt.from_xy(vx - 1, ay)
        collect.add(npt)
    if vx <= cpt.x(ep) <= ax:
        collect.add(cpt.from_xy(cpt.x(ep), ay))

    for hy in hk:
        if hy < ay:
            continue
        npt = cpt.from_xy(ax, hy - 1)
        if npt != at:
            collect.add(npt)
        if ax in h_segs[hy]:
            break
        npt = cpt.from_xy(ax, hy + 1)
        collect.add(npt)
    if ay <= cpt.y(ep) <= hy:
        collect.add(cpt.from_xy(ax, cpt.y(ep)))

    for hy in r_hk:
        if hy > ay:
            continue
        npt = cpt.from_xy(ax, hy + 1)
        if npt != at:
            collect.add(npt)
        if ax in h_segs[hy]:
            break
        npt = cpt.from_xy(ax, hy - 1)
        collect.add(npt)
    if hy <= cpt.y(ep) <= ay:
        collect.add(cpt.from_xy(ax, cpt.y(ep)))

    return collect

def part3(output=False):
    instrs = parse('data/ec_2025/15-c.txt')

    h_segs, v_segs, ep = make_segs(instrs)
    hk = sorted(h_segs)
    vk = sorted(v_segs)
    r_hk = sorted(h_segs, reverse=True)
    r_vk = sorted(v_segs, reverse=True)

    ngh = Dictlike(partial(find_moves, h_segs, hk, r_hk, v_segs, vk, r_vk, ep))
    dst = Dictlike(lambda pp: int(cpt.m_dist(pp[0], pp[1])))
    wts = dijkstra(ngh, dst, start_point=cpt.ZERO, end_point=ep, keep_paths=False)
    return wts[ep]
