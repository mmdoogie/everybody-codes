from collections import defaultdict

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip() for l in f.readlines()]
    conv = {}
    for l in lines:
        k, v = l.split(':')
        conv[k] = v.split(',')
    return conv

def compute(conv, start, days):
    have = defaultdict(int)
    have[start] = 1
    for _ in range(days):
        next_round = defaultdict(int)
        for h in have:
            for c in conv[h]:
                next_round[c] += have[h]
        have = next_round
    return sum(have.values())

def part1(output):
    conv = parse('data/ec_2024/11-a.txt')
    return compute(conv, 'A', 4)

def part2(output):
    conv = parse('data/ec_2024/11-b.txt')
    return compute(conv, 'Z', 10)

def part3(output):
    conv = parse('data/ec_2024/11-c.txt')
    res = [compute(conv, c, 20) for c in conv]
    return max(res) - min(res)
