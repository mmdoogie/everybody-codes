from collections import Counter

from mrm.parse import all_nums

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return list(all_nums(lines[0]))

def part1(output=False):
    crates = sorted(parse('data/ec_2025/03-a.txt'), reverse=True)

    box_size = crates[0]
    box_cap = crates[0]

    for c in crates:
        if c < box_size:
            box_size = c
            box_cap += c

    return box_cap

def part2(output=False):
    crates = sorted(parse('data/ec_2025/03-b.txt'))

    box_size = crates[0]
    box_cap = crates[0]
    box_cnt = 1

    for c in crates:
        if c > box_size:
            box_size = c
            box_cap += c
            box_cnt += 1
        if box_cnt == 20:
            break

    return box_cap

def part3(output=False):
    crates = sorted(parse('data/ec_2025/03-c.txt'), reverse=True)

    set_cnt = 0

    # Thinking about how to optimize this after the fact, a maxheap or way to keep all of the current smallest boxes
    # works, but then it becomes obvious that you'll start with however many of the largest boxes, then they consume
    # that many of every smaller size. So you have to expand the set by however many of the largest non-consumed one
    # are left, and eventually it turns into the number of boxes in the most populous size.
    if False:
        return max(Counter(crates).values())

    while crates:
        box_size = crates[0]
        set_cnt += 1
        skip = []

        for c in crates[1:]:
            if c < box_size:
                box_size = c
            else:
                skip += [c]

        crates = skip

    return set_cnt
