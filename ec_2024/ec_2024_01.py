from mrm.iter import batched

def read_file(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = f.readlines()
    return lines[0].strip()

def part1(output):
    amt = {'A': 0, 'B': 1, 'C': 3}
    dat = read_file('data/ec_2024/01-a.txt')
    return sum(amt[d] for d in dat)

def pair_cost(pair):
    amt = {'A': 0, 'B': 1, 'C': 3, 'D': 5, 'x': 0}
    cost = sum(amt[p] for p in pair)
    if 'x' in pair:
        return cost
    return cost + 2

def part2(output):
    dat = read_file('data/ec_2024/01-b.txt')
    return sum(pair_cost(d) for d in batched(dat, batch_size=2))

def trio_cost(trio):
    amt = {'A': 0, 'B': 1, 'C': 3, 'D': 5, 'x': 0}
    cost = sum(amt[t] for t in trio)
    xcnt = sum(t == 'x' for t in trio)
    if xcnt == 0:
        return cost + 2*3
    if xcnt == 1:
        return cost + 2
    return cost

def part3(output):
    dat = read_file('data/ec_2024/01-c.txt')
    return sum(trio_cost(d) for d in batched(dat, batch_size=3))
