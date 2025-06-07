from mrm.parse import all_nums

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return [all_nums(l) for l in lines]

def eni(n, exp, mod):
    rems = []
    score = 1
    for _ in range(exp):
        score = (score * n) % mod
        rems += [score]
    return int(''.join(str(x) for x in reversed(rems)))

def part1(output=False):
    lines = parse('data/ec_1/01-a.txt')
    max_v = 0
    for l in lines:
        a, b, c, x, y, z, m = l
        v = eni(a, x, m) + eni(b, y, m) + eni(c, z, m)
        max_v = max(max_v, v)
        if output:
            print((a, x, m), (b, y, m), (c, z, m), v)
    return max_v

def eni5(n, exp, mod):
    rems = []
    for i in range(exp - 4, exp + 1):
        rems += [pow(n, i, mod)]
    return int(''.join(str(x) for x in reversed(rems)))

def part2(output=False):
    lines = parse('data/ec_1/01-b.txt')
    max_v = 0
    for l in lines:
        a, b, c, x, y, z, m = l
        v = eni5(a, x, m) + eni5(b, y, m) + eni5(c, z, m)
        max_v = max(max_v, v)
        if output:
            print((a, x, m), (b, y, m), (c, z, m), v)
    return max_v

def eniall(n, exp, mod):
    rems = []
    offset = 0
    for i in range(1, mod):
        r = pow(n, i, mod)
        if r in rems:
            offset = rems.index(r)
            break
        rems += [r]
    rv = sum(rems[:offset])
    rems = rems[offset:]
    exp -= offset
    rv += sum(rems) * (exp // len(rems))
    rv += sum(rems[:exp % len(rems)])
    return rv

def part3(output=False):
    lines = parse('data/ec_1/01-c.txt')
    max_v = 0
    for l in lines:
        a, b, c, x, y, z, m = l
        v = eniall(a, x, m) + eniall(b, y, m) + eniall(c, z, m)
        max_v = max(max_v, v)
        if output:
            print((a, x, m), (b, y, m), (c, z, m), v)
    return max_v
