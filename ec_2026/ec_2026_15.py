from collections import defaultdict
from functools import partial
import math
import operator

import mrm.ansi_term as ansi
from mrm.bitvector import Bitvector
import mrm.cpoint as cpt
from mrm.dijkstra import Dictlike, dijkstra
import mrm.image as img

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid, inv = cpt.grid_as_dict(lines, valid=lambda x: x not in '#', with_inv=True)
    return grid, inv

def part1(output=False):
    grid, inv = parse('data/ec_2026/15-a.txt')

    sulphurs = list(inv['@'])

    def ngh(at):
        pos, sulph, heading = at
        adj = set()

        for h in [heading, cpt.left_turn(heading), cpt.right_turn(heading)]:
            next_pos = pos + h
            if next_pos not in grid:
                continue
            if next_pos in sulphurs:
                adj.add((next_pos, sulph.copy_with(sulphurs.index(next_pos)), h))
            else:
                adj.add((next_pos, sulph, h))
        return adj

    sp = (inv['S'].pop(), Bitvector(max_bit=len(sulphurs)), cpt.RIGHT)
    ep = (inv['E'].pop(), Bitvector(max_bit=len(sulphurs), iv=2 ** len(sulphurs) - 1), cpt.RIGHT)
    wt, p = dijkstra(Dictlike(ngh), start_point=sp, end_point=ep, dist_est=lambda x: cpt.m_dist(x[0], ep[0]))

    if output:
        res_path = [x[0] for x in p[ep]]
        def disp_ch(x, y, c):
            pt = cpt.from_xy(x, y)
            if pt not in grid:
                return '#'
            if pt in res_path:
                if c == '.':
                    return ansi.green('+')
                return ansi.red(c)
            return c
        img.print_image(grid, use_char=True, highlighter=disp_ch)

    return wt[ep]

def compress(grid, inv):
    s_pt = list(inv['S'])[0]
    e_pt = list(inv['E'])[0]

    ngh = defaultdict(set)
    wts = {}
    slp = {}
    at = s_pt
    while at != e_pt:
        for cont_head in [cpt.LEFT, cpt.RIGHT]:
            if at + cont_head not in grid:
                continue
            for from_head in [cont_head, cpt.UP, cpt.DOWN]:
                ngh[(at, from_head)].add((at + cont_head, cont_head))
                wts[((at, from_head), (at + cont_head, cont_head))] = 1
                slp[((at, from_head), (at + cont_head, cont_head))] = 0

        for turn_head in [cpt.UP, cpt.DOWN]:
            if at + turn_head not in grid:
                continue
            trace = at + turn_head
            trace_h = turn_head
            trace_s = 0
            trace_w = 1
            while cpt.y(trace) != cpt.y(at):
                trace_w += 1
                if trace in inv['@']:
                    trace_s += 1
                if trace + trace_h not in grid:
                    if trace_h in [cpt.UP, cpt.DOWN]:
                        if trace + cpt.LEFT in grid:
                            trace_h = cpt.LEFT
                        else:
                            trace_h = cpt.RIGHT
                    else:
                        trace_h = -turn_head
                trace += trace_h
            for cont_head in [cpt.LEFT, cpt.RIGHT]:
                ngh[(at, cont_head)].add((trace, trace_h))
                wts[((at, cont_head), (trace, trace_h))] = trace_w
                slp[((at, cont_head), (trace, trace_h))] = trace_s
            ngh[(at, turn_head)].add((trace, trace_h))
            wts[((at, turn_head), (trace, trace_h))] = trace_w
            slp[((at, turn_head), (trace, trace_h))] = trace_s

        at += cpt.RIGHT

    return ngh, wts, slp

def part2(output=False):
    grid, inv = parse('data/ec_2026/15-b.txt')
    ngh_dict, wts_dict, slp = compress(grid, inv)

    def ngh(x):
        at, at_sulph = x
        adj = {(n, at_sulph + slp[(at, n)]) for n in ngh_dict[at]}
        return adj

    def wts(x):
        (fm, _), (to, _) = x
        return wts_dict[(fm, to)]

    s_point = inv['S'].pop()
    e_point = inv['E'].pop()
    start_node = ((s_point, cpt.RIGHT), 0)
    end_node   = ((e_point, cpt.RIGHT), 2026 + 50)
    dists = dijkstra(Dictlike(ngh), Dictlike(wts), start_node, end_node, keep_paths=False)
    best_dist = min(v for k, v in dists.items() if k[0][0] == e_point and k[1] >= 2026)

    return best_dist

def part3(output=False):
    grid, inv = parse('data/ec_2026/15-c.txt')
    ngh_dict, wts_dict, slp = compress(grid, inv)

    sulph_tgt = 202620262026

    max_loop = None
    loop_vals = (0, 1)
    for k, v in slp.items():
        if v == 0:
            continue
        (fm, _), (to, to_head) = k
        if cpt.x(fm) > cpt.x(to):
            continue
        vals = (v, wts_dict[k])
        if operator.truediv(*vals) > operator.truediv(*loop_vals):
            max_loop = ((fm, to_head), (to, to_head))
            loop_vals = vals

    def ngh(prune, x):
        at, at_sulph = x
        if prune < at_sulph < sulph_tgt - prune:
            return {}
        if at[1] is None:
            at = (at[0], to_head)
        adj = {(n, at_sulph + slp[(at, n)]) for n in ngh_dict[at]}
        return adj

    def wts(x):
        (fm, _), (to, _) = x
        if fm[1] is None:
            return wts_dict[((fm[0], to_head), to)]
        return wts_dict[(fm, to)]

    s_point = inv['S'].pop()
    e_point = inv['E'].pop()

    moves = 0
    remain = sulph_tgt
    loop_cnt = remain // loop_vals[0] - 5
    if loop_cnt % 2 == 1:
        loop_cnt -= 1
    remain -= loop_vals[0] * loop_cnt
    moves += loop_vals[1] * loop_cnt

    ngh_dict[(max_loop[0][0], cpt.RIGHT)].add((max_loop[0][0], None))
    wts_dict[((max_loop[0][0], cpt.RIGHT), (max_loop[0][0], None))] = moves
    slp[((max_loop[0][0], cpt.RIGHT), (max_loop[0][0], None))] = loop_vals[0] * loop_cnt

    start_node = ((s_point, cpt.RIGHT), 0)
    end_node = ((e_point, cpt.RIGHT), sulph_tgt)
    wt, p = dijkstra(Dictlike(partial(ngh, 500)), Dictlike(wts), start_node, end_node, keep_paths=True)

    if output:
        res_path = [ps[0][0] for ps in p[end_node]]
        print(res_path)
        def disp_ch(x, y, c):
            pt = cpt.from_xy(x, y)
            if pt not in grid:
                return '#'
            if pt in res_path:
                if c == '.':
                    return ansi.green('+')
                return ansi.red(c)
            return c
        img.print_image(grid, use_char=True, highlighter=disp_ch)

    return wt[end_node]
