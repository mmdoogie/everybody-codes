def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse('data/ec_4/01-a.txt')

    tot = 0
    for l in lines:
        moves = [int(x) for x in l.split(',')]
        curr_pt = 0
        hit = set()
        for m in moves:
            next_pt = curr_pt - m
            if next_pt <= 0 or next_pt in hit:
                next_pt = curr_pt + m
            curr_pt = next_pt
            hit.add(curr_pt)
        tot += curr_pt

        if output:
            print(f'{l} ends at {curr_pt}')

    return tot

def part2(output=False):
    lines = parse('data/ec_4/01-b.txt')

    tot = 0
    for l in lines:
        moves = [int(x) for x in l.split(',')]
        curr_pt = 0
        hit = set()
        for m in moves:
            next_pt = curr_pt - m
            if next_pt <= 0 or next_pt in hit:
                next_pt = curr_pt + m
            while next_pt in hit:
                next_pt += 1
            curr_pt = next_pt
            hit.add(curr_pt)
        tot += curr_pt

        if output:
            print(f'... {l[-10:]} ends at {curr_pt}')

    return tot

def check_arc(left, right, arcs):
    for a in arcs.items():
        if left < a[0] < right < a[1]:
            return False
        if a[0] < left < a[1] < right:
            return False

    return True

def part3(output=False):
    lines = parse('data/ec_4/01-c.txt')
    tot = 0

    for l in lines:
        moves = [int(x) for x in l.split(',')]

        curr_pt = 0
        max_pt = 0
        on_top = False

        hit = set()
        top_arcs = {}
        bot_arcs = {}

        for m in moves:
            arcs = top_arcs if on_top else bot_arcs
            next_pt = curr_pt - m
            if next_pt <= 0 or next_pt in hit or not check_arc(next_pt, curr_pt, arcs):
                next_pt = curr_pt + m

            skip = False
            while next_pt in hit or not check_arc(curr_pt, next_pt, arcs):
                next_pt += 1
                if next_pt > max_pt + 1:
                    skip = True
                    break
            if skip:
                continue

            hit.add(next_pt)
            arcs[min(curr_pt, next_pt)] = max(curr_pt, next_pt)
            curr_pt = next_pt
            on_top = not on_top
            max_pt = max(max_pt, curr_pt)

        tot += curr_pt

        if output:
            print(f'... {l[-10:]} ends at {curr_pt}')

    return tot
