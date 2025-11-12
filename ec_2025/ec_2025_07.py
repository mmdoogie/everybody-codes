from collections import defaultdict
from itertools import combinations, pairwise

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    names = lines[0].split(',')
    rules = defaultdict(set)
    for l in lines[2:]:
        lh, rh = l.split(' > ')
        rh = rh.split(',')
        rules[lh].update(rh)
    return names, rules

def part1(output=False):
    names, rules = parse('data/ec_2025/07-a.txt')

    for n in names:
        for a, b in pairwise(n):
            if b not in rules[a]:
                break
        else:
            return n

    return ''

def part2(output=False):
    names, rules = parse('data/ec_2025/07-b.txt')

    ok_names = 0
    for i, n in enumerate(names):
        for a, b in pairwise(n):
            if b not in rules[a]:
                break
        else:
            ok_names += (i + 1)

    return ok_names

def part3(output=False):
    names, rules = parse('data/ec_2025/07-c.txt')

    ok_names = set()
    for n in names:
        for a, b in pairwise(n):
            if b not in rules[a]:
                break
        else:
            ok_names.add(n)

    included_names = set()
    for a, b in combinations(ok_names, 2):
        if a in b:
            included_names.add(b)
        if b in a:
            included_names.add(a)

    total_names = 0
    for n in ok_names - included_names:
        curr_ending = {n[-1]: 1}
        for l in range(len(n) + 1, 12):
            next_ending = defaultdict(int)
            for k, v in curr_ending.items():
                for nxt in rules[k]:
                    next_ending[nxt] += v
            if l >= 7:
                total_names += sum(next_ending.values())
            curr_ending = next_ending

    return total_names
