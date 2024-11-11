from collections import defaultdict

from mrm.dijkstra import dijkstra

def file_lines(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip() for l in f.readlines()]
    return lines

def find_strongest(lines, abbrev = False):
    ngh = {}
    i = 0
    for l in lines:
        s = l.split(':')
        k = s[0]
        v = s[1].split(',')
        if '@' in v:
            v[v.index('@')] = f'@{i}'
            i += 1
        ngh[k] = v

    _, p = dijkstra(ngh, start_point='RR')

    path_by_len = defaultdict(list)
    for k, v in p.items():
        if not k.startswith('@'):
            continue
        if abbrev:
            path = ''.join([x[0] for x in v[:-1]]) + '@'
        else:
            path = ''.join(v[:-1]) + '@'
        path_by_len[len(v)] += [path]

    for k, v in path_by_len.items():
        if len(v) != 1:
            continue
        return v[0]

def part1(output):
    lines = file_lines('data/ec_2024/06-a.txt')
    return find_strongest(lines, abbrev=False)

def part2(output):
    lines = file_lines('data/ec_2024/06-b.txt')
    return find_strongest(lines, abbrev=True)

def part3(output):
    lines = file_lines('data/ec_2024/06-c.txt')
    return find_strongest(lines, abbrev=True)
