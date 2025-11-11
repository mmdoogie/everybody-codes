from collections import defaultdict
import string

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines[0]

def part1(output=False):
    line = parse('data/ec_2025/06-a.txt')
    sword_lets = [l for l in line if l in 'Aa']

    cnt = 0
    for i, l in enumerate(sword_lets):
        if l == 'a':
            continue
        cnt += sum(l == 'a' for l in sword_lets[i+1:])

    return cnt

def part2(output=False):
    line = parse('data/ec_2025/06-b.txt')

    cnt = 0
    for uc, lc in zip(string.ascii_uppercase, string.ascii_lowercase):
        lets = [l for l in line if l in uc + lc]
        for i, l in enumerate(lets):
            if l == lc:
                continue
            cnt += sum(l == lc for l in lets[i+1:])

    return cnt

def part3(output=False):
    line = parse('data/ec_2025/06-c.txt')

    max_dist = 1000
    line_len = len(line)
    reps = 1000

    locs = defaultdict(set)
    for i, l in enumerate(line):
        locs[l].add(i)

    cnt = 0
    edge = 0
    for uc, lc in zip(string.ascii_uppercase, string.ascii_lowercase):
        for pos in locs[lc]:
            for pmp in range(pos - max_dist, pos + max_dist + 1):
                wrap = False
                if pmp < 0:
                    pmp = line_len + pmp
                    wrap = True
                if pmp >= line_len:
                    pmp = pmp - line_len
                    wrap = True
                if pmp in locs[uc]:
                    cnt += 1
                    if wrap:
                        edge += 1

    return cnt * reps - edge
