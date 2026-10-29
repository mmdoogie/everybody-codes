from itertools import cycle

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    pairs = []
    for l in lines:
        standard, vote = l.split(' ')
        base = standard.split('-')[1]
        pairs += [(base, vote)]
    return pairs

def from_base(base, vote):
    val = 0
    for i, (b, v) in enumerate(zip(cycle(reversed(base)), reversed(vote))):
        val += int(v) * (int(b) ** i)
    return val

def part1(output=False):
    pairs = parse('data/ec_2026/03-a.txt')
    score = 0
    for base, vote in pairs:
        score += from_base(base, vote)
    return score

def part2(output=False):
    pairs = parse('data/ec_2026/03-b.txt')
    score = 0
    for base, vote in pairs:
        score += from_base(base, vote)
    return score

def part3(output=False):
    pairs = parse('data/ec_2026/03-c.txt')
    score = 0
    for base, vote in pairs:
        vote_val = from_base(base, vote)
        for x in range(int(vote) - 1, 1, -1):
            v = from_base(base, str(x))
            if v == vote_val:
                if output:
                    print(f'Found lower vote {x}, {vote} -> {v} in ISO2-{base}')
                break
        else:
            score += vote_val
    return score
