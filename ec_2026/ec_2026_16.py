from collections import defaultdict

import mrm.ansi_term as ansi
from mrm.util import fastreverse_deque

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines[0]

COLORS = {'R': ansi.red, 'G': ansi.green, 'B': ansi.blue, 'Y': ansi.yellow}

def do_sort(pattern, *, count_swap_items=False, output=False):
    working = fastreverse_deque(pattern)
    match = working.popleft()
    swaps = 0
    pfx = defaultdict(int)

    discard = fastreverse_deque()
    while working:
        while working and working[0] == match:
            working.popleft()
            pfx[match] += 1

        if not working:
            break

        while working and working[-1] != match:
            discard.append(working.pop())

        if not working:
            working, discard = discard, working
            working.reverse()
            match = working.popleft()
            pfx[match] += 1
            discard.clear()
            continue

        working.reverse()
        if count_swap_items:
            swaps += len(working)
        else:
            swaps += 1

        if output:
            recon_pat  = [COLORS[k](k * v) for k, v in pfx.items()]
            recon_pat += [COLORS[c](c)     for c    in working]
            recon_pat += [COLORS[c](c)     for c    in discard]
            print(''.join(recon_pat))

    return swaps

def part1(output=False):
    pattern = parse('data/ec_2026/16-a.txt')
    return do_sort(pattern, output=output)

def part2(output=False):
    pattern = parse('data/ec_2026/16-b.txt') * 10
    return do_sort(pattern, count_swap_items=True)

def part3(output=False):
    pattern = parse('data/ec_2026/16-c.txt') * 100
    return do_sort(pattern, count_swap_items=True)
