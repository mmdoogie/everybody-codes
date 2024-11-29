def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse('data/ec_{YEAR}/{DAY}-a.txt')
    return ''

def part2(output=False):
    lines = parse('data/ec_{YEAR}/{DAY}-b.txt')
    return ''

def part3(output=False):
    lines = parse('data/ec_{YEAR}/{DAY}-c.txt')
    return ''
