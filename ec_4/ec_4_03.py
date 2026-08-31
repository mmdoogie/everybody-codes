from itertools import cycle

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    width, height, h_offs, v_offs = None, None, None, None

    for l in lines:
        lh, rh = l.split('=')
        match lh:
            case 'width':
                width = int(rh)
            case 'height':
                height = int(rh)
            case 'horizontal-offsets':
                h_offs = [int(x) for x in rh]
            case 'vertical-offsets':
                v_offs = [int(x) for x in rh]

    return width, height, h_offs, v_offs

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

def part1(output=False):
    width, height, h_offs, v_offs = parse('data/ec_4/03-a.txt')

    cells = {(x, y): [False, False, False, False]
        for x in range(width + 1) for y in range(height + 1)}

    offsets = cycle(h_offs)
    for y in range(height + 1):
        o = next(offsets)
        for x in range(width):
            cells[(x, y)][UP] = (x + o + 1) % 2
            if y != 0:
                cells[(x, y - 1)][DOWN] = (x + o + 1) % 2

    offsets = cycle(v_offs)
    for x in range(width + 1):
        o = next(offsets)
        for y in range(height):
            cells[(x, y)][LEFT] = (y + o + 1) % 2
            if x != 0:
                cells[(x - 1, y)][RIGHT] = (y + o + 1) % 2

    if output:
        for y in range(height):
            for x in range(width):
                print('#' if sum(cells[(x, y)]) == 4 else '.', end='')
            print()

    return sum(sum(c) == 4 for c in cells.values())

def part2(output=False):
    width, height, h_offs, v_offs = parse('data/ec_4/03-b.txt')

    curr_color = True
    start_color = True

    col_cnts = [0, 0]

    hpat_len = len(v_offs) * 2
    hpat_mul = width // hpat_len
    hpat_rem = width % hpat_len

    vpat_len = len(h_offs) * 2
    vpat_mul = height // vpat_len
    vpat_rem = height % vpat_len

    for x in range(hpat_len):
        for y in range(vpat_len):
            left = (y + v_offs[x % len(v_offs)] + 1) % 2
            right = (y + v_offs[(x + 1) % len(v_offs)] + 1) % 2
            up = (x + h_offs[y % len(h_offs)] + 1) % 2
            down = (x + h_offs[(y + 1) % len(h_offs)] + 1) % 2

            if y == 0:
                if left:
                    start_color = not start_color
                curr_color = start_color

            if y != 0 and up:
                curr_color = not curr_color

            if up and left and down and right:
                col_cnts[curr_color] += (hpat_mul + int(x < hpat_rem)) * (vpat_mul + int(y < vpat_rem))
                if output:
                    print('@' if curr_color else '#', end='')
            elif output:
                print('.' if curr_color else '-', end='')
        if output:
            print()

    return max(col_cnts)

def part3(output=False):
    width, height, h_offs, v_offs = parse('data/ec_4/03-c.txt')

    curr_color = True
    start_color = True

    col_cnts = [0, 0]

    hpat_len = len(v_offs) * 2
    hpat_mul = width // hpat_len
    hpat_rem = width % hpat_len

    vpat_len = len(h_offs) * 2
    vpat_mul = height // vpat_len
    vpat_rem = height % vpat_len

    for x in range(hpat_len):
        for y in range(vpat_len):
            left = (y + v_offs[x % len(v_offs)] + 1) % 2
            right = (y + v_offs[(x + 1) % len(v_offs)] + 1) % 2
            up = (x + h_offs[y % len(h_offs)] + 1) % 2
            down = (x + h_offs[(y + 1) % len(h_offs)] + 1) % 2

            if y == 0:
                if left:
                    start_color = not start_color
                curr_color = start_color

            if y != 0 and up:
                curr_color = not curr_color

            if up and left and down and right:
                col_cnts[curr_color] += (hpat_mul + int(x < hpat_rem)) * (vpat_mul + int(y < vpat_rem))

    return max(col_cnts)
