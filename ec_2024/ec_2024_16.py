from collections import Counter, deque
from math import lcm, inf

from mrm.cache import keycache
from mrm.parse import ensure_equal_length

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return ensure_equal_length(lines)

def part1(output):
    lines = parse('data/ec_2024/16-a.txt')

    incrs = [int(x) for x in lines[0].split(',')]
    num_wheels = len(incrs)
    wheels = [[l[w*4:w*4+3] for l in lines[2:]] for w in range(num_wheels)]
    wheel_sizes = [w.index('   ') if '   ' in w else len(w) for w in wheels]

    idx = [(100 * i) % s for i, s in zip(incrs, wheel_sizes)]
    return ' '.join(wheels[n][x] for n, x in enumerate(idx))

@keycache
def wheel_score(wheels, idx, *, key):
    vis = ''.join(wheels[n][x][::2] for n, x in enumerate(idx))
    cnt = Counter(vis)
    score = 0
    for _, c in cnt.most_common():
        if c < 3:
            break
        score += c - 2
    return score

def part2(output):
    lines = parse('data/ec_2024/16-b.txt')

    incrs = [int(x) for x in lines[0].split(',')]
    num_wheels = len(incrs)
    wheels = [[l[w*4:w*4+3] for l in lines[2:]] for w in range(num_wheels)]
    wheel_sizes = [w.index('   ') if '   ' in w else len(w) for w in wheels]

    idx = [(100 * i) % s for i, s in zip(incrs, wheel_sizes)]

    repeat_len = lcm(*wheel_sizes)
    goal = 202420242024
    repeat_cnt = goal // repeat_len
    addon_cnt = goal % repeat_len

    score = 0
    for n in range(1, repeat_len + 1):
        idx = tuple((n * i) % s for i, s in zip(incrs, wheel_sizes))
        score += (repeat_cnt + (1 if n <= addon_cnt else 0)) * wheel_score(wheels, idx, key=idx)

    return score

@keycache
def leverpull(idx, left_pull, incrs, wheel_sizes, *, key):
    return tuple((x + i + left_pull) % s for x, i, s in zip(idx, incrs, wheel_sizes))

def part3(output):
    lines = parse('data/ec_2024/16-c.txt')

    incrs = [int(x) for x in lines[0].split(',')]
    num_wheels = len(incrs)
    wheels = [[l[w*4:w*4+3] for l in lines[2:]] for w in range(num_wheels)]
    wheel_sizes = [w.index('   ') if '   ' in w else len(w) for w in wheels]

    idx = tuple(0 for i in incrs)
    state = (idx, 256, 0)
    to_explore = deque([state])
    seen = set()
    min_score = inf
    max_score = 0
    while to_explore:
        src_idx, pulls_remain, src_score = to_explore.pop()
        if pulls_remain == 0:
            min_score = min(min_score, src_score)
            max_score = max(max_score, src_score)
            continue
        for left_pull in [-1, 0, 1]:
            dst_idx = leverpull(src_idx, left_pull, incrs, wheel_sizes, key=(src_idx, left_pull))
            dst_score = src_score + wheel_score(wheels, dst_idx, key=dst_idx)
            new_state = (dst_idx, pulls_remain - 1, dst_score)
            if new_state not in seen:
                to_explore.append(new_state)
                seen.add(new_state)

    return f'{max_score} {min_score}'
