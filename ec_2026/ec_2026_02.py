from functools import cmp_to_key, partial
from string import digits

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    cmp_dicts = []
    for l in lines:
        pairs = l.split(' ')
        cmps = {}
        for p in pairs:
            a, s, b = p
            cmp_val = -1 if s == '<' else 1
            cmps[(a, b)] = cmp_val
            cmps[(b, a)] = -cmp_val
        cmp_dicts += [cmps]
    return cmp_dicts

def cmp_missing(cmp, a, b, output):
    if (a, b) in cmp:
        if output:
            print(a, '<' if cmp[(a, b)] < 0 else '>', b)
        return cmp[(a, b)]
    for d in digits:
        if (a, d) in cmp and (d, b) in cmp and cmp[(a, d)] == cmp[(d, b)]:
            if output:
                print(a, '<' if cmp[(a, d)] < 0 else '>', b, 'inferred via', d)
            return cmp[(a, d)]
    raise ValueError(f'Comparison {a} to {b} impossible with single inference')

def do_sort(cmp_dicts, output):
    tot = 0
    for cmp in cmp_dicts:
        chk = list({a for a, _ in cmp})
        if output:
            print('Sorting', ''.join(chk))
        sort_key = cmp_to_key(partial(cmp_missing, cmp, output=output))
        chk.sort(key=sort_key, reverse=True)
        val = int(''.join(chk))
        if output:
            print(val)
        tot += val
    return tot

def part1(output=False):
    cmp_dicts = parse('data/ec_2026/02-a.txt')
    return do_sort(cmp_dicts, output)

def part2(output=False):
    cmp_dicts = parse('data/ec_2026/02-b.txt')
    return do_sort(cmp_dicts, output)

def part3(output=False):
    cmp_dicts = parse('data/ec_2026/02-c.txt')
    return do_sort(cmp_dicts, output)
