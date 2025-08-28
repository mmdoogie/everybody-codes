from collections import deque
from itertools import cycle

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse('data/ec_2/02-a.txt')
    balloons = lines[0]
    bolts = cycle('RGB')

    curr_bolt = next(bolts)
    cnt = 1
    for b in balloons:
        issued = False
        if b == curr_bolt:
            continue
        curr_bolt = next(bolts)
        cnt += 1
        issued = True
    return cnt - 1 if issued else 0

def part2(output=False):
    lines = parse('data/ec_2/02-b.txt')
    b_near = deque(lines[0] * (100 // 2))
    b_far = deque(lines[0] * (100 // 2))
    bolts = cycle('RGB')

    curr_bolt = next(bolts)
    cnt = 1
    remain = len(b_near) + len(b_far)
    while True:
        n = b_near.popleft()
        if remain % 2 == 0:
            f = b_far.popleft()
            if n != curr_bolt:
                b_near.append(f)
            else:
                remain -= 1
        remain -= 1
        if remain == 0:
            break
        curr_bolt = next(bolts)
        cnt += 1

    return cnt

def part3(output=False):
    lines = parse('data/ec_2/02-c.txt')
    b_near = deque(lines[0] * 50000)
    b_far = deque(lines[0] * 50000)
    bolts = cycle('RGB')

    curr_bolt = next(bolts)
    cnt = 1
    remain = len(b_near) + len(b_far)
    while True:
        n = b_near.popleft()
        if remain % 2 == 0:
            f = b_far.popleft()
            if n != curr_bolt:
                b_near.append(f)
            else:
                remain -= 1
        remain -= 1
        if remain == 0:
            break
        curr_bolt = next(bolts)
        cnt += 1

    return cnt
