def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse('data/ec_2025/13-a.txt')
    turns = 2025

    nums = [int(x) for x in lines]
    wheel = [1]

    for i, n in enumerate(nums):
        if i % 2 == 0:
            wheel = wheel + [n]
        else:
            wheel = [n] + wheel

    ctr_idx = wheel.index(1)

    return wheel[(ctr_idx + turns) % len(wheel)]

def do_turns(ranges, turns):
    l_cnt, r_cnt = 0, 0
    alloc = []
    for i, r in enumerate(ranges):
        left = i % 2 == 1
        in_rng = r[1] - r[0]
        if left:
            alloc += [(r[0], left, l_cnt, l_cnt + in_rng)]
            l_cnt += in_rng + 1
        else:
            alloc += [(r[0], left, r_cnt, r_cnt + in_rng)]
            r_cnt += in_rng + 1

    wheel_size = 1 + sum(mx - mn + 1 for _, _, mn, mx in alloc)
    dest = (l_cnt + turns) % wheel_size

    if dest == l_cnt:
        return 1

    if dest < l_cnt:
        dest = l_cnt - dest - 1
        left = True
    else:
        dest = dest - l_cnt - 1
        left = False

    for r in alloc:
        if r[1] != left:
            continue
        if r[2] <= dest <= r[3]:
            return r[0] + dest - r[2]

    raise IndexError


def part2(output=False):
    lines = parse('data/ec_2025/13-b.txt')
    ranges = [tuple(int(v) for v in l.split('-')) for l in lines]

    return do_turns(ranges, 20252025)

def part3(output=False):
    lines = parse('data/ec_2025/13-c.txt')
    ranges = [tuple(int(v) for v in l.split('-')) for l in lines]

    return do_turns(ranges, 202520252025)
