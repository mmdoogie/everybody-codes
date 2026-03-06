from collections import defaultdict
import string

def txt_to_bin(txt):
    bin_txt = ['0' if t in string.ascii_lowercase else '1' for t in txt]
    return int(''.join(bin_txt), 2)

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    pats = {}
    for l in lines:
        id_str, rgbs = l.split(':')
        pats[int(id_str)] = [txt_to_bin(v) for v in rgbs.split(' ')]
    return pats

def part1(output=False):
    pats = parse('data/ec_3/01-a.txt')
    return sum(p[0] for p in filter(lambda x: x[1][1] > x[1][0] and x[1][1] > x[1][2], pats.items()))

def part2(output=False):
    pats = parse('data/ec_3/01-b.txt')
    max_shine = max(v[3] for v in pats.values())
    is_max = filter(lambda x: x[1][3] == max_shine, pats.items())
    is_min = min(is_max, key=lambda x: sum(x[1][:3]))
    return is_min[0]

def part3(output=False):
    pats = parse('data/ec_3/01-c.txt')
    grps = defaultdict(list)
    for pid, rgbs in pats.items():
        if 31 <= rgbs[3] <= 32:
            continue
        shiny = rgbs[3] >= 33

        max_rgb = max(rgbs[:3])
        if sum(r == max_rgb for r in rgbs[:3]) > 1:
            continue
        color_idx = rgbs[:3].index(max_rgb)

        grps[(color_idx, shiny)] += [pid]
    big_grp = max(grps.items(), key=lambda x: len(x[1]))
    return sum(big_grp[1])
