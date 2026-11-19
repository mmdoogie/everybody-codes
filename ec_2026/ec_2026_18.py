import mrm.ansi_term as ansi
from mrm.parse import all_nums

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    nums = [list(all_nums(l)) for l in lines]
    return nums

def part1(output=False):
    nums = parse('data/ec_2026/18-a.txt')
    hts = {n[0]: n[1] for n in nums}
    left, right = min(hts), max(hts)

    in_pat = set()
    for x in range(left, right + 1):
        if x not in hts:
            continue
        for y in range(hts[x]):
            in_pat.add((x, y))
            maybe = set()
            for x2 in range(x + 1, right + 1):
                maybe.add((x2, y))
                if x2 in hts and hts[x2] - 1 >= y:
                    break
            else:
                maybe.clear()
            in_pat.update(maybe)

    if output:
        height = max(hts.values())
        for y in range(height, 0, -1):
            print(f'{y:2} ', end='')
            for x in range(left, right + 1):
                if (x, y) in in_pat:
                    if x in hts:
                        print(ansi.red('#'), end='')
                    else:
                        print(ansi.green('='), end='')
                else:
                    print(ansi.cyan('.'), end='')
            print()
        print('   ', end='')
        for x in range(left, right + 1):
            print(x % 10, end='')
        print()

    return len(in_pat)

def part2(output=False):
    nums = parse('data/ec_2026/18-b.txt')
    hts = {x2: y for x, y, w in nums for x2 in range(x, x + w)}
    left, right = min(hts), max(hts)

    in_pat = set()
    for x in range(left, right + 1):
        if x not in hts:
            continue
        for y in range(hts[x]):
            in_pat.add((x, y))
            maybe = set()
            for x2 in range(x + 1, right + 1):
                maybe.add((x2, y))
                if x2 in hts and hts[x2] - 1 >= y:
                    break
            else:
                maybe.clear()
            in_pat.update(maybe)

    return len(in_pat)

def part3(output=False):
    nums = parse('data/ec_2026/18-c.txt')

    cnt = 0
    for i, (x, y, col_width) in enumerate(nums):
        cnt += col_width * y
        if output:
            print(f'├┬ At {x}: {col_width} * {y} = {col_width * y}')
        processed_ht = 0
        x += col_width - 1
        for x2, y2, _ in nums[i + 1:]:
            if y2 <= processed_ht:
                continue
            y2 = min(y2, y)
            added_width = x2 - x + 1 - 2
            cnt += (added_width * (y2 - processed_ht))
            if output:
                print(f'│├── adj above {processed_ht}: {added_width} * {y2 - processed_ht} = {added_width * (y2 - processed_ht)}')
            processed_ht = y2
            if processed_ht == y:
                break

    return cnt
