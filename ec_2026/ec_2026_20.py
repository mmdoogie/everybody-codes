from collections import defaultdict
from itertools import permutations

from numpy import base_repr

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

class SevSeg:
    def __init__(self, segs):
        if len(segs) != 7 and len(segs) != 10:
            raise ValueError("10 segment values required")
        if any(not isinstance(x, bool) for x in segs):
            raise ValueError("segment values must be bool")
        if len(segs) == 7:
            self._segs = tuple(segs + [False]*3)
        else:
            self._segs = tuple(segs)

    def __hash__(self):
        return hash(self._segs)

    def __len__(self):
        return sum(self._segs)

    def __sub__(self, oth):
        if (self.is_sym() and not oth.is_sym()) or self._segs[9] or oth._segs[9]:
            raise ValueError("-/+ can only change to opposite, cannot mutate '='")
        diff = sum(a != b for a, b in zip(self._segs, oth._segs))
        sign = 1 if len(self) > len(oth) else -1
        return diff * sign

    def __str__(self):
        if self._segs[8]:
            return '\n'.join(['   ', '   ', ' + ', '   ', '   '])
        if self._segs[9]:
            return '\n'.join(['   ', '   ', ' = ', '   ', '   '])
        if self._segs[7]:
            return '\n'.join(['   ', '   ', ' - ', '   ', '   '])
        a = ' ━ ' if self._segs[0] else '   '
        b = '┃ ' if self._segs[1] else '  '
        c = ' ━ ' if self._segs[2] else '   '
        d = '┃ ' if self._segs[3] else '  '
        e = ' ━ ' if self._segs[4] else '   '
        f = '┃' if self._segs[5] else ' '
        g = '┃' if self._segs[6] else ' '
        return '\n'.join([a, b+f, c, d+g, e])

    def is_sym(self):
        return self._segs[7]

SEGS = {'0': SevSeg([True, True, False, True, True, True, True]),
        '1': SevSeg([False, False, False, False, False, True, True]),
        '2': SevSeg([True, False, True, True, True, True, False]),
        '3': SevSeg([True, False, True, False, True, True, True]),
        '4': SevSeg([False, True, True, False, False, True, True]),
        '5': SevSeg([True, True, True, False, True, False, True]),
        '6': SevSeg([True, True, True, True, True, False, True]),
        '7': SevSeg([True, False, False, False, False, True, True]),
        '8': SevSeg([True]*7),
        '9': SevSeg([True, True, True, False, True, True, True]),
        'A': SevSeg([True, True, True, True, False, True, True]),
        '+': SevSeg([False]*7+[True, True, False]),
        '-': SevSeg([False]*7+[True,False, False]),
        '=': SevSeg([False]*7+[True,False,True])}

def print_sevseg(line, suffix=None):
    strs = [str(SEGS[c]) if c in SEGS else f' \n \n{c}\n \n ' for c in line]
    if suffix:
        strs += [f'\n\n {suffix}\n\n']
    for bunch in zip(*(s.split('\n') for s in strs)):
        print(''.join(bunch))

def eval_in_base(expr, base):
    left, op, right = expr.split(' ')
    if op == '-':
        return int(left, base) - int(right, base)
    return int(left, base) + int(right, base)

def part1(output=False):
    lines = parse('data/ec_2026/20-a.txt')
    cnt = 0
    for l in lines:
        left, right = l.split(' = ')
        if eval_in_base(left, 10) == eval_in_base(right, 10):
            val = sum(len(SEGS[s]) for s in l if s in SEGS)
            cnt += val
            if output:
                print_sevseg(l, f'({val} segs)')
        elif output:
            print_sevseg(l, 'INVALID!')
    return cnt

def check_line(l):
    left, right = l.split(' = ')
    if eval_in_base(left, 11) == eval_in_base(right, 11):
        return sum(len(SEGS[s]) for s in l if s in SEGS)
    return 0

def part2(output=False):
    lines = parse('data/ec_2026/20-b.txt')
    cnt = 0
    for l in lines:
        val = check_line(l)
        if val:
            cnt += val
            if output:
                print_sevseg(l, f'({val} segs)')
        elif output:
            print_sevseg(l, 'INVALID!')
    return base_repr(cnt, 11)

def construct_repairs():
    repair_donor = defaultdict(list)
    repair_acceptor = defaultdict(list)
    repair_trans = defaultdict(list)
    for a, b in permutations(SEGS, 2):
        try:
            diff = SEGS[a] - SEGS[b]
            if diff == 1:
                repair_donor[a] += [b]
            if diff == -1:
                repair_acceptor[a] += [b]
            if not SEGS[a].is_sym() and not SEGS[b].is_sym() and (len(SEGS[a]) == len(SEGS[b])):
                repair_trans[a] += [b]
        except ValueError:
            pass
    return repair_donor, repair_acceptor, repair_trans

def try_repair(repair_donor, repair_acceptor, repair_trans, l, output):
    tries = 0
    for i, lc in enumerate(l):
        for r in repair_trans.get(lc, []):
            trans_line = l[:i] + r + l[i + 1:]
            val = check_line(trans_line)
            tries += 1
            if val:
                if output:
                    print_sevseg(f'{l} to {trans_line}')
                return val, tries

        for r in repair_donor.get(lc, []):
            donor_line = l[:i] + r + l[i + 1:]
            for j, c2 in enumerate(donor_line):
                for r2 in repair_acceptor.get(c2, []):
                    if i == j and lc == r2:
                        continue
                    repair_line = donor_line[:j] + r2 + donor_line[j + 1:]
                    val = check_line(repair_line)
                    tries += 1
                    if val:
                        if output:
                            print_sevseg(f'{l} to {repair_line}')
                        return val, tries
    return 0, tries

def part3(output=False):
    lines = parse('data/ec_2026/20-c.txt')
    repair_donor, repair_acceptor, repair_trans = construct_repairs()

    if output:
        print("Segment Donors")
        for fm, to_l in repair_donor.items():
            for to in to_l:
                print_sevseg(f'{fm} to {to}')
        print("Segment Acceptors")
        for fm, to_l in repair_acceptor.items():
            for to in to_l:
                print_sevseg(f'{fm} to {to}')
        print("Trans Segments")
        for fm, to_l in repair_trans.items():
            for to in to_l:
                print_sevseg(f'{fm} to {to}')

    seg_cnt = 0
    need_repair = 0
    all_tries = 0
    for l in lines:
        val = check_line(l)
        if val:
            if output:
                print_sevseg(l)
            seg_cnt += val
            continue

        need_repair += 1
        val, tries = try_repair(repair_donor, repair_acceptor, repair_trans, l, output)
        all_tries += tries
        if val:
            seg_cnt += val
            continue

    if output:
        print(f'Avg. repair trials per line: {all_tries/need_repair:0.2f}')

    return base_repr(seg_cnt, 11)
