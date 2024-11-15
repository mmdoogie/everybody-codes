def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip() for l in f.readlines()]
    return [int(x) for x in lines]

def part1(output):
    balls = parse('data/ec_2024/09-a.txt')
    stamps = sorted([1, 3, 5, 10], reverse=True)

    tot = 0
    for b in balls:
        remain = b
        for s in stamps:
            add = remain // s
            tot += add
            remain -= s * add
    return tot

def build_cost(max_b, stamps):
    sorted_stamps = sorted(stamps, reverse=True)
    cost = {0: 0}
    for b in range(1, max_b + 1):
        cost[b] = min(1 + cost[b - s] for s in sorted_stamps if b - s in cost)
    return cost

def part2(output):
    balls = parse('data/ec_2024/09-b.txt')
    stamps = [1, 3, 5, 10, 15, 16, 20, 24, 25, 30]

    cost = build_cost(max(balls), stamps)
    return sum(cost[b] for b in balls)

def part3(output):
    balls = parse('data/ec_2024/09-c.txt')
    stamps = [1, 3, 5, 10, 15, 16, 20, 24, 25, 30, 37, 38, 49, 50, 74, 75, 100, 101]

    cost = build_cost(max(balls) // 2 + 50, stamps)

    total = 0
    for b in balls:
        midp = b // 2
        opts = []
        left = midp
        right = midp + (midp % 2)
        inc_left = False
        while right - left <= 100:
            opts += [cost[right] + cost[left]]
            left -= 1 if inc_left else 0
            right += 0 if inc_left else 1
            inc_left = not inc_left
        total += min(opts)
    return total
