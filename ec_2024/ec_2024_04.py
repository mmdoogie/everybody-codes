def get_nails(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip() for l in f.readlines()]
    return [int(l) for l in lines]

def part1(output):
    nails = get_nails('data/ec_2024/04-a.txt')
    min_nail = min(nails)
    return sum(n - min_nail for n in nails)

def part2(output):
    nails = get_nails('data/ec_2024/04-b.txt')
    min_nail = min(nails)
    return sum(n - min_nail for n in nails)

def part3(output):
    nails = get_nails('data/ec_2024/04-c.txt')

    level = int(sum(nails) / len(nails))
    min_hits = sum(abs(n - level) for n in nails)

    step = 1
    level += step
    result = sum(abs(n - level) for n in nails)
    if result > min_hits:
        step = -step

    while True:
        level += step
        result = sum(abs(n - level) for n in nails)
        if result > min_hits:
            break
        min_hits = result
    return min_hits
