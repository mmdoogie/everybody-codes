from fractions import Fraction
from itertools import pairwise
import math

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [int(l.strip('\n')) for l in f.readlines()]
    return lines

def sim_rounds(ducks, num_cols, num_rounds, output, skip_phase2=False):
    rounds = 0

    if output:
        duck_str = ', '.join(f'{d:2}' for d in ducks)
        print(f'Round: {rounds:2}, Ducks: {duck_str}')
        print('Phase 1')

    # phase 1
    moved = True
    while moved:
        moved = False
        for a, b in pairwise(range(num_cols)):
            if ducks[a] > ducks[b]:
                ducks[a] -= 1
                ducks[b] += 1
                moved = True
        if not moved:
            break
        rounds += 1
        if output:
            duck_str = ', '.join(f'{d:2}' for d in ducks)
            print(f'Round: {rounds:2}, Ducks: {duck_str}')
        if rounds == num_rounds:
            break

    if output:
        print('Phase 2')

    if skip_phase2:
        return ducks, rounds

    # phase 2
    moved = True
    while moved:
        moved = False
        for a, b in pairwise(range(num_cols)):
            if ducks[a] < ducks[b]:
                ducks[b] -= 1
                ducks[a] += 1
                moved = True
        if not moved:
            break
        rounds += 1
        if output:
            duck_str = ', '.join(f'{d:2}' for d in ducks)
            print(f'Round: {rounds:2}, Ducks: {duck_str}')
        if rounds == num_rounds:
            break

    return ducks, rounds

def part1(output=False):
    ducks = parse('data/ec_2025/11-a.txt')

    ducks, _ = sim_rounds(ducks, len(ducks), 10, output)

    return sum(i*d for i, d in enumerate(ducks, 1))

def count_moves(ducks, output):
    ducks = [Fraction(d) for d in ducks]
    num_cols = len(ducks)

    moves = 0
    while True:
        # Since we are starting with a sorted list from phase 1:
        # Every pass, we can move some number of ducks from the columns with the most
        # to the columns with the least.  If there are multiple columns with the same
        # number of ducks, then they will pass along to each other and act as a group
        # source/sink.  Calculate how many can be sent/received, and do the minimum,
        # which brings that group close to even with its adjacent columns.  Then the
        # group will be able to grow and work as a larger group.  When there are only
        # two groups remaining, the final balancing only needs to send what it takes
        # to even them up.
        deltas = [a - b for a, b in pairwise(ducks) if a - b > 0]
        send_cols = sum(d == max(ducks) for d in ducks)
        recv_cols = sum(d == min(ducks) for d in ducks)

        re_delt = deltas[-1]
        rcv_max = re_delt * recv_cols
        le_delt = deltas[0]
        snd_max = le_delt * send_cols

        if send_cols + recv_cols == num_cols:
            xfer = le_delt * (send_cols * recv_cols) / (send_cols + recv_cols)
        else:
            xfer = min(snd_max, rcv_max)

        moves += xfer

        for i in range(send_cols):
            ducks[i] -= xfer / send_cols

        for i in range(recv_cols):
            ducks[-i-1] += xfer / recv_cols

        if output:
            print(f'Moving {int(xfer):13} ducks from {send_cols:2} cols to {recv_cols:2} cols. ', end='')
            print(f'Total moves {int(moves):15}. Max: {str(max(ducks)):18}, Min: {str(min(ducks)):18}')

        if send_cols + recv_cols == num_cols:
            break

    return moves

def part2(output=False):
    ducks = parse('data/ec_2025/11-b.txt')

    ducks, rounds = sim_rounds(ducks, len(ducks), math.inf, False, skip_phase2=True)
    rounds += count_moves(reversed(ducks), output)

    return rounds

def part3(output=False):
    ducks = parse('data/ec_2025/11-c.txt')

    moves = count_moves(reversed(ducks), output)

    return moves
