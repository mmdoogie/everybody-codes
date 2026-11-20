from collections import Counter
from itertools import permutations

import mrm.ansi_term as ansi
from mrm.util import big_pi

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    try:
        split = lines.index('')
    except ValueError:
        return lines
    return [lines[:split], lines[split + 1:]]

def add_colors(a, b):
    if a == 'K' or b == 'K':
        return 'K'
    if ord(a) > ord(b):
        a, b = b, a
    if a == 'C' and b == 'M':
        return 'B'
    if a == 'C' and b == 'Y':
        return 'G'
    if a == 'M' and b == 'Y':
        return 'R'
    assert a == b
    return a

COLORS = {'R': ansi.red, 'G': ansi.green, 'B': ansi.blue,
          'C': ansi.cyan, 'M': ansi.magenta, 'Y': ansi.yellow,
          'K': lambda c: ' '}

def part1(output=False):
    layers = parse('data/ec_2026/19-a.txt')

    cnt = Counter()
    res_layer = []
    for y in zip(*layers):
        res_row = []
        for x in zip(*y):
            res = add_colors(*x)
            res_row += [res]
            cnt[res] += 1
        res_layer += [res_row]
    top_vals = [m[1] for m in cnt.most_common(3)]

    if output:
        for i, l in enumerate(layers + [res_layer]):
            print('Layer', i)
            for y in l:
                for x in y:
                    print(COLORS[x](x), end='')
                print()
            print()
        print('Counts:', cnt.most_common())

    return big_pi(top_vals)

def part2(output=False):
    layers = parse('data/ec_2026/19-b.txt')

    max_val = 0
    for cmb in permutations('CMYK', 4):
        num_map = {str(i + 1): c for i, c in enumerate(cmb)}
        cnt = Counter()
        res_layer = []
        for y in zip(*layers):
            res_row = []
            for x in zip(*y):
                res = add_colors(x[0], num_map[x[1]])
                res_row += [res]
                cnt[res] += 1
            res_layer += [res_row]

        if output and max_val == 0:
            for y in res_layer:
                for x in y:
                    print(COLORS[x](x), end='')
                print()

        top_vals = [m[1] for m in cnt.most_common(3)]
        val = big_pi(top_vals)
        if val > max_val:
            max_val = val

    return max_val

def part3(output=False):
    layer = parse('data/ec_2026/19-c.txt')
    cnt = Counter(''.join(layer))
    total = sum(m[1] for m in cnt.most_common(3))
    nums = [total // 3] * 3
    for r in range(total % 3):
        nums[r] += 1
    if output:
        print('Counts:       ', cnt.most_common())
        print('Top 3 Total:  ', total)
        print('Result Counts:', nums)

    return big_pi(nums)
