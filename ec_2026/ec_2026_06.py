from mrm.dijkstra import dijkstra

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    ingr_lists = {}
    for l in lines:
        name, ingr_list = l.split(':')
        ingrs = ingr_list.split(',')
        ingr_lists[name] = set(ingrs)
    return ingr_lists

def part1(output=False):
    ingr_lists = parse('data/ec_2026/06-a.txt')
    reach = dijkstra(ingr_lists, start_point='NULL', keep_paths=False)
    return len(reach) - 1

def part2(output=False):
    ingr_lists = parse('data/ec_2026/06-b.txt')

    cnt = 0
    for i in ingr_lists:
        reach = dijkstra(ingr_lists, start_point=i, end_point='NULL', keep_paths=False)
        if 'NULL' in reach:
            cnt += 1

    return cnt

def part3(output=False):
    ingr_lists = parse('data/ec_2026/06-c.txt')
    end_nodes = [f'NULLv{x}' for x in range(1, 4)]

    cnt = 0
    for i in ingr_lists:
        reach = dijkstra(ingr_lists, start_point=i, end_point=end_nodes, keep_paths=False)
        if sum(en in reach for en in end_nodes) >= 2:
            cnt += 1

    return cnt
