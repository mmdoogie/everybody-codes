from itertools import cycle, product
from math import lcm

import mrm.cpoint as pt

def trace_track(lines):
    width = max(len(l) for l in lines)
    height = len(lines)
    lines = [f'{l:<{width}}' for l in lines]

    pos = pt.ZERO
    head = pt.RIGHT
    track = []

    while True:
        pos = pt.go_dist(pos, head, 1)
        x, y = pt.as_xy(pos, int)

        if x >= width or x < 0 or y >= height or y < 0 or lines[y][x] == ' ':
            pos = pt.go_dist(pos, head, -1)
            head = pt.left_turn(head)
            pos = pt.go_dist(pos, head, 1)
            x, y = pt.as_xy(pos, int)

            if x >= width or x < 0 or y >= height or y < 0 or lines[y][x] == ' ':
                head = pt.u_turn(head)
                pos = pt.go_dist(pos, head, 2)
                x, y = pt.as_xy(pos, int)

        ch = lines[y][x]
        track += [ch]
        if ch == 'S':
            return ''.join(track)

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip() for l in f.readlines()]

    patterns = {}
    for l in lines:
        if l[0] in 'S+-=':
            continue
        name, actions = l.split(':')
        actions = actions.split(',')
        patterns[name] = ''.join(actions)

    track_lines = [l for l in lines if l[0] in 'S+-=']
    if not track_lines:
        return patterns

    track = trace_track(track_lines)
    return patterns, track

def part1(output):
    patterns = parse('data/ec_2024/07-a.txt')

    results = {}
    for name, pat in patterns.items():
        pwr = 10
        tot = 0

        for _, act in zip(range(10), cycle(pat)):
            if act == '+':
                pwr += 1
            if act == '-' and pwr > 0:
                pwr -= 1
            tot += pwr
        results[name] = tot

    return ''.join(x[0] for x in sorted(results.items(), key=lambda x: x[1], reverse=True))

def run_pat_on_track(track, pat, loops=10):
    pwr = 10
    tot = 0
    pat = cycle(pat)

    for _ in range(loops):
        for t_act in track:
            c_act = next(pat)

            if t_act == '+':
                c_act = '+'
            elif t_act == '-':
                c_act = '-'

            if c_act == '+':
                pwr += 1
            elif c_act == '-' and pwr > 0:
                pwr -= 1

            tot += pwr
    return tot, pwr

def part2(output):
    knights, track = parse('data/ec_2024/07-b.txt')
    pwr = {k: run_pat_on_track(track, v) for k, v in knights.items()}
    return ''.join(x[0] for x in sorted(pwr.items(), key=lambda x: x[1], reverse=True))

def run_pat_on_track_faster(track, pat, loops):
    track_len = len(track)
    incr_rounds = lcm(track_len, len(pat)) // len(track)
    assert loops % incr_rounds == 0

    score_inc, pwr = run_pat_on_track(track, pat, incr_rounds)
    score = score_inc
    pwr_inc = pwr - 10
    for _ in range(loops // incr_rounds - 1):
        score += score_inc + (pwr - 10) * track_len * incr_rounds
        pwr += pwr_inc
    return score

def wins(track, pat, tgt):
    if sum(p=='+' for p in pat) != 5 or sum(p=='-' for p in pat) != 3:
        return False
    score = run_pat_on_track_faster(track, pat, 2024)
    return score > tgt

def part3(output):
    k, t = parse('data/ec_2024/07-c.txt')
    them  = run_pat_on_track_faster(t, k['A'], 2024)
    syms = ['-', '+', '=']
    all_pat = product(syms, repeat=11)
    return sum(wins(t, p, them) for p in all_pat)
