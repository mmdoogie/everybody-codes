def get_input(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip() for l in f.readlines()]
    return int(lines[0])

def part1(output):
    blocks_avail = get_input('data/ec_2024/08-a.txt')
    layer = 1
    width = 1
    used = 0
    while True:
        used += width
        if output:
            print('Layer', layer, 'width', width, 'used', used)
        if used > blocks_avail:
            return width * (used - blocks_avail)
        layer += 1
        width += 2
    return 0

def part2(output):
    priests = get_input('data/ec_2024/08-b.txt')
    acolytes = 1111
    blocks_avail = 20240000
    layer = 1
    width = 1
    thickness = 1
    used = 0
    while True:
        used += width * thickness
        if output:
            print('Layer', layer, 'width', width, 'thickness', thickness, 'used', used)
        if used > blocks_avail:
            return width * (used - blocks_avail)
        thickness = (thickness * priests) % acolytes
        layer += 1
        width += 2
    return 0

def empty_space(cols, hp, ha):
    tot = 0
    for c in cols[1:-1]:
        rem = (hp * len(cols) * c) % ha
        tot += rem
    return tot

def part3(output):
    high_priests = get_input('data/ec_2024/08-c.txt')
    high_acolytes = 10
    blocks_avail = 202400000
    layer = 1
    thickness = 1
    cols = [1]
    while True:
        thickness = (thickness * high_priests) % high_acolytes + high_acolytes
        cols = [thickness] + [c + thickness for c in cols] + [thickness]
        hollow = empty_space(cols, high_priests, high_acolytes)
        used = sum(cols) - hollow
        if output:
            print(f'Layer {layer} width {len(cols)} thickness {thickness} if solid {sum(cols)} but hollow {hollow} so used {used}')
        if used > blocks_avail:
            return used - blocks_avail
        layer += 1
    return ''
