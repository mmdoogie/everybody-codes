from collections import Counter, defaultdict
from math import lcm, inf

from mrm.cache import Keycache
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

@Keycache(stats=True)
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

@Keycache(stats=True)
def leverpull(idx, left_pull, incrs, wheel_sizes, *, key):
    return tuple((x + i + left_pull) % s for x, i, s in zip(idx, incrs, wheel_sizes))

def part3(output):
    lines = parse('data/ec_2024/16-c.txt')

    incrs = [int(x) for x in lines[0].split(',')]
    num_wheels = len(incrs)
    wheels = [[l[w*4:w*4+3] for l in lines[2:]] for w in range(num_wheels)]
    wheel_sizes = [w.index('   ') if '   ' in w else len(w) for w in wheels]

    state = tuple(0 for i in incrs)
    pull_mins = {state: 0}
    pull_maxs = {state: 0}
    to_explore = [state]

    for pull in range(256):
        next_explore = set()
        next_nonunique = 0
        next_mins = defaultdict(lambda:inf)
        next_maxs = defaultdict(lambda:0)

        for state in to_explore:
            for left_pull in [-1, 0, 1]:
                new_state = leverpull(state, left_pull, incrs, wheel_sizes, key=(state, left_pull))
                score = wheel_score(wheels, new_state, key=new_state)
                next_explore.add(new_state)
                next_nonunique += 1
                next_mins[new_state] = min(next_mins[new_state], pull_mins[state] + score)
                next_maxs[new_state] = max(next_maxs[new_state], pull_maxs[state] + score)
        to_explore, pull_mins, pull_maxs = next_explore, next_mins, next_maxs
        if output:
            print(f'Pull {pull:>3d} -> {next_nonunique:>4d} states ({len(to_explore):>3d} unique)', end=' ')
            print(f'min {min(pull_mins.values()):>2d} max {max(pull_maxs.values()):>3d}')

    if output:
        hits, misses = leverpull.stats()
        calls = hits + misses
        print(f'Lever Pull  Cache: {calls:>8d} calls {hits:>8d} hits ({hits/calls*100:6.2f}%), {misses:>8d} misses ({misses/calls*100:6.2f}%)')
        hits, misses = wheel_score.stats()
        calls = hits + misses
        print(f'Wheel Score Cache: {calls:>8d} calls {hits:>8d} hits ({hits/calls*100:6.2f}%), {misses:>8d} misses ({misses/calls*100:6.2f}%)')

    return f'{max(pull_maxs.values())} {min(pull_mins.values())}'
