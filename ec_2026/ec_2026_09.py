from collections import defaultdict

from mrm.parse import all_nums

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    trees = [tuple(all_nums(l)) for l in lines]
    return trees

def part1(output=False):
    trees = parse('data/ec_2026/09-a.txt')

    tot_sec = 0
    for tree, growth, limit in trees:
        if output:
            print(f'Tree {tree} splits at {growth} limit {limit}')
        ts = 0
        branches = 0
        growing = [0]
        while branches + sum(growing) < limit:
            growing = [g + 1 for g in growing]
            splits = sum(1 for g in growing if g == growth)
            branches += splits
            growing = [g if g != growth else 1 for g in growing]
            growing += [growth // 2] * (2 * splits)
            ts += 1
            if output:
                print(f'ts {ts:2}: elements {branches + sum(growing)}')
        tot_sec += ts
        if output:
            print('LIMIT\n')

    return tot_sec

def part2(output=False):
    trees = parse('data/ec_2026/09-b.txt')

    tot_sec = 0
    for tree, growth, limit in trees:
        if output:
            print(f'Tree {tree} splits at {growth} limit {limit}')
        ts = 0
        branches = 0
        growing = [0]
        while len(growing) - branches < limit:
            growing = [g + 1 for g in growing]
            splits = sum(1 for g in growing if g == growth)
            branches += splits
            growing = [g if g != growth else 1 for g in growing]
            growing += [growth // 2] * (2 * splits)
            ts += 1
            if output:
                print(f'ts {ts:3}: leaves {len(growing) - branches}')
        tot_sec += ts
        if output:
            print('LIMIT\n')

    return tot_sec

def part3(output=False):
    trees = parse('data/ec_2026/09-c.txt')

    tot_sec = 0
    for tree, growth, limit in trees:
        if output:
            print(f'Tree {tree} splits at {growth} limit {limit}')
        if limit < growth:
            tot_sec += limit
            continue
        next_splits = defaultdict(int)
        next_splits[growth] = 1
        splits = 0
        ts = 0
        step_cnt = 0
        while sum(next_splits.values()) - splits < limit:
            ts = min(next_splits)
            cnt = next_splits[ts]

            next_splits[ts +  growth - 1] += cnt
            next_splits[ts + growth // 2 + 1] += 2 * cnt
            splits += cnt
            step_cnt += 1

            del next_splits[ts]
            if output:
                print(f'step {step_cnt:3} @ ts {ts:15}: leaves {sum(next_splits.values()) - splits}')
        tot_sec += ts
        if output:
            print('LIMIT\n')
    return tot_sec
