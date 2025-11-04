def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    names = lines[0].split(',')
    instrs = lines[2].split(',')
    return names, instrs

def part1(output=False):
    names, instrs = parse('data/ec_2025/01-a.txt')

    name_count = len(names)
    if output:
        print('Name count:', name_count)

    idx = 0
    for i in instrs:
        match i[0]:
            case 'L':
                idx -= min(int(i[1:]), idx)
            case 'R':
                idx += min(int(i[1:]), name_count - 1 - idx)
        if output:
            print(i, 'now at', idx)

    return names[idx]

def part2(output=False):
    names, instrs = parse('data/ec_2025/01-b.txt')

    name_count = len(names)
    if output:
        print('Name count:', name_count)

    idx = 0
    for i in instrs:
        match i[0]:
            case 'L':
                idx -= int(i[1:])
            case 'R':
                idx += int(i[1:])
        if output:
            print(i, 'now at', idx % name_count)

    return names[idx % name_count]

def part3(output=False):
    names, instrs = parse('data/ec_2025/01-c.txt')

    name_count = len(names)
    if output:
        print('Name count:', name_count)

    nl = dict(enumerate(names))

    for i in instrs:
        match i[0]:
            case 'L':
                idx = -int(i[1:]) % name_count
            case 'R':
                idx =  int(i[1:]) % name_count
        if output:
            print(i, 'swapping idx', 0, idx, 'names', nl[idx], nl[0])
        nl[0], nl[idx] = nl[idx], nl[0]

    return nl[0]
