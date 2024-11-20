from math import inf

def get_lines(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip() for l in f.readlines()]
    return lines

def get_targets(lines):
    tgts = []
    srcs = []
    hard = []
    max_y = len(lines) - 2
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c in 'TH':
                tgts += [(x, max_y - y)]
                hard += [2 if c == 'H' else 1]
            if c in 'ABC':
                srcs += [(x, max_y - y)]
    return tgts, srcs, hard

def get_power(src, tgt):
    dx = tgt[0] - src[0]
    dy = tgt[1] - src[1]

    # Only on ascending phase if dx=dy
    if dx == dy:
        return int(dx) * (1 + src[1])

    # On horizontal phase, have to have gone up by dy
    # and have less remaining x than the dy
    if dx - dy <= dy:
        return int(dy) * (1 + src[1])

    # For descending phase, again a dx=dy check, but after some travel
    # After p, we're at x = xs + 2*p and y = ys + p
    # so only on descending if (xt - xs - 2*p) = (ys + p - yt)
    # and if that's the case then solve for p = (dx + dy) / 3
    if (dx + dy) % 3 == 0:
        return (dx + dy) // 3 * (1 + src[1])

    return inf

def part1(output):
    lines = get_lines('data/ec_2024/12-a.txt')
    tgts, srcs, _ = get_targets(lines)

    tot = sum(min(get_power(s, t) for s in srcs) for t in tgts)
    return int(tot)

def part2(output):
    lines = get_lines('data/ec_2024/12-b.txt')
    tgts, srcs, hard = get_targets(lines)

    tot = sum(h * min(get_power(s, t) for s in srcs) for t, h in zip(tgts, hard))
    return int(tot)

def get_power_meteor(src, nd_tgt):
    for delay in range(10):
        tgt = (nd_tgt[0] - delay, nd_tgt[1] - delay)
        dx = tgt[0] - src[0]
        dy = tgt[1] - src[1]

        # Ascending, must have dx == dy,
        # min power hit / max height would be at dx / 2
        p = dx // 2
        if dx == dy and dx % 2 == 0:
            return (p + src[1], p * (1 + src[1]))

        # Horizontal, write x & y in terms of power p and additional time t
        # xs + p + t = xt - p - t -> dx = 2p + 2t
        # ys + p     = yt - p - t -> dy = 2p +  t
        # Then t = dx - dy and p = dy - dx / 2
        # Also check that 0 < t <= p, since outside of that we are not horizontal
        t = dx - dy
        p = dy - dx // 2
        if dx % 2 == 0 and 0 < t <= p:
            return (p + src[1], p * (1 + src[1]))

        # Descending, similar setup
        # xs + 2p + t = xt - 2p - t -> dx = 4p + 2t
        # ys +  p - t = yt - 2p - t -> dy = 3p
        # t = dx / 2 - 2 * dy / 3 and p = dy / 3
        # Check t > 0
        t = dx // 2 - 2 * dy // 3
        p = dy // 3
        if dy % 3 == 0 and dx % 2 == 0 and t > 0:
            return (p + src[1], p * (1 + src[1]))

    return (-1, inf)

def part3(output):
    lines = get_lines('data/ec_2024/12-c.txt')

    srcs = [(0, 0), (0, 1), (0, 2)]
    meteors = []
    for l in lines:
        x, y = l.split(' ')
        meteors += [(int(x), int(y))]

    tot = 0
    for m in meteors:
        pwrs = [get_power_meteor(s, m) for s in srcs]
        tot += max(pwrs, key = lambda x: (x[0], -x[1]))[1]
    return int(tot)
