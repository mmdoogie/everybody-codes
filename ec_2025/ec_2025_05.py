from dataclasses import dataclass

from mrm.parse import all_nums

@dataclass
class Layer:
    center: int
    left: int = None
    right: int = None

    def __str__(self):
        return ''.join(str(s) for s in [self.left, self.center, self.right] if s)

    def score(self):
        return int(str(self))

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [list(all_nums(l.strip('\n'))) for l in f.readlines()]

    return [[l[0], l[1:]] for l in lines]

def qual(vals, *, with_layers = False, part3_id = None):
    layers = [Layer(vals[0])]
    for v in vals[1:]:
        placed = False
        for l in layers:
            if not l.left and v < l.center:
                l.left = v
                placed = True
                break
            if not l.right and v > l.center:
                l.right = v
                placed = True
                break
        if not placed:
            layers += [Layer(v)]

    spine = int(''.join(str(l.center) for l in layers))

    if with_layers:
        return spine, layers

    if not part3_id:
        return spine

    return (spine, tuple(l.score() for l in layers), part3_id)

def part1(output=False):
    swords = parse('data/ec_2025/05-a.txt')

    if not output:
        return qual(swords[0][1])

    score, layers = qual(swords[0][1], with_layers=True)
    print(r'*/ \*')
    print('  |  ')
    for l in layers:
        print(f'{l.left if l.left else " "}-{l.center}-{l.right if l.right else " "}')
        print('  |  ')
    print(r' / \ ')

    return score

def part2(output=False):
    swords = parse('data/ec_2025/05-b.txt')

    spines = {s[0]: qual(s[1]) for s in swords}

    if output:
        for sk, sv in spines.items():
            print(f'{sk:3}: {sv}')

    return max(spines.values()) - min(spines.values())

def part3(output=False):
    swords = parse('data/ec_2025/05-c.txt')

    scores = sorted((qual(s[1], part3_id = s[0]) for s in swords), reverse=True)

    if output:
        for i, s in enumerate(scores):
            print(f'{i:3}: {s}')

    return sum((i + 1) * s[2] for i, s in enumerate(scores))
