from fractions import Fraction as F
from itertools import combinations

from mrm.parse import all_nums

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    offset = 0
    while offset < len(lines):
        hands = list(all_nums(lines[offset + 0]))
        dirs = [{'CCW': -1, 'CW': 1}[d]  for d in lines[offset + 1].split(' ')[1].split(':')]
        curr = list(all_nums(lines[offset + 2]))
        move = list(all_nums(lines[offset + 3]))
        offset += 5

        yield hands, dirs, curr, move

def check_signal(ia, ib):
    if ia[1] % 1 == ib[1] % 1:
        return ((ia[0] != ia[1]) or (ib[0] != ib[1])) and (ia[0] != ib[0])

    if ia[1] < 0:
        ia = (ia[0] + 1, ia[1] + 1)

    if ib[1] < 0:
        ib = (ib[0] + 1, ib[1] + 1)

    n = ib[0] - ia[0]
    d = (ia[1] - ia[0]) - (ib[1] - ib[0])

    if d != 0 and n != 0:
        t = n / d
        if 0 < t < 1:
            return 1
    return 0

def part1(output=False):
    clocks = parse('data/ec_2026/13-a.txt')
    hands, dirs, curr, move = next(clocks)

    hands_per = [F(d, h) for d, h in zip(dirs, hands)]
    at = [c * abs(hp) for c, hp in zip(curr, hands_per)]

    sigs = 0
    for tick in range(1, max(move) + 1):
        intervals = [(a, (a + hp) if tick <= m else a) for a, hp, m in zip(at, hands_per, move)]
        for i_pair in combinations(intervals, 2):
            chk = check_signal(*i_pair)
            sigs += chk
            if chk and output:
                print(f'tick {tick:2} sigs {sigs}')
        at = [i[1] % 1 for i in intervals]

    return sigs

def part2(output=False):
    clocks = parse('data/ec_2026/13-b.txt')

    total = 0
    for hands, dirs, curr, move in clocks:
        hands_per = [F(d, h) for d, h in zip(dirs, hands)]
        at = [c * abs(hp) for c, hp in zip(curr, hands_per)]

        sigs = 0
        for tick in range(1, max(move) + 1):
            intervals = [(a, (a + hp) if tick <= m else a) for a, hp, m in zip(at, hands_per, move)]
            for i_pair in combinations(intervals, 2):
                sigs += check_signal(*i_pair)
            at = [i[1] % 1 for i in intervals]

        if output:
            print(sigs)
        total += sigs

    return total

def part3(output=False):
    clocks = parse('data/ec_2026/13-c.txt')

    total = 0
    for hands, dirs, curr, move in clocks:
        if output:
            print('\nclock move', move)

        hands_per = [F(d, h) for d, h in zip(dirs, hands)]
        at = [c * abs(hp) for c, hp in zip(curr, hands_per)]

        loop_cfg = tuple(at)
        loop_tick = 0
        loop_sigs = 0

        sigs = 0
        tick = 0
        while tick <= max(move):
            tick += 1
            intervals = [(a, (a + hp) if tick <= m else a) for a, hp, m in zip(at, hands_per, move)]
            for i_pair in combinations(intervals, 2):
                sigs += check_signal(*i_pair)
            at = tuple(i[1] % 1 for i in intervals)
            if at == loop_cfg:
                remain = 0
                for m in sorted(move):
                    if m > tick:
                        remain = m - tick
                        break
                if remain == 0:
                    break
                full_copies = remain // (tick - loop_tick)
                if output:
                    print(f'loop at tick {tick}, remain {remain}, copies {full_copies}')
                tick += full_copies * (tick - loop_tick)
                sigs += full_copies * (sigs - loop_sigs)
                if output:
                    print(f'now at {tick} with {sigs}')

                loop_tick = tick
                loop_sigs = sigs

            if any(tick == m for m in move):
                loop_cfg = at
                loop_tick = tick
                loop_sigs = sigs
        if output:
            print(sigs)
        total += sigs
    return total
