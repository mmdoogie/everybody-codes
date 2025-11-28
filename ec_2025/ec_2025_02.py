import mrm.ansi_term as ansi
from mrm.parse import all_nums

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return tuple(all_nums(lines[0]))

def part1(output=False):
    a = parse('data/ec_2025/02-a.txt')

    rx, ry = 0, 0
    for _ in range(3):
        rx, ry = int((rx * rx - ry * ry) / 10) + a[0], int((rx * ry + rx * ry) / 10) + a[1]

    return f'[{rx},{ry}]'

def part2(output=False):
    a = parse('data/ec_2025/02-b.txt')

    palette = [ansi.red, ansi.magenta, ansi.blue, ansi.cyan, ansi.green, ansi.yellow]

    engrave = 0
    for y in range(0, 1001, 10):
        for x in range(0, 1001, 10):
            rx, ry = 0, 0
            px, py = x + a[0], y + a[1]
            ok = True
            for i in range(100):
                rx, ry = int((rx * rx - ry * ry) / 100000) + px, int((rx * ry + rx * ry) / 100000) + py
                ok = -1000000 <= rx <= 1000000 and -1000000 <= ry <= 1000000
                if not ok:
                    break
            if output:
                print(palette[(i-21)//14]('**') if not ok else '  ', end='')
            if ok:
                engrave += 1
        if output:
            print()

    return engrave

def part3(output=False):
    a = parse('data/ec_2025/02-c.txt')

    engrave = 0
    for y in range(0, 1001):
        for x in range(0, 1001):
            rx, ry = 0, 0
            px, py = x + a[0], y + a[1]
            ok = True
            for i in range(100):
                rx, ry = int((rx * rx - ry * ry) / 100000) + px, int((rx * ry + rx * ry) / 100000) + py
                ok = -1000000 <= rx <= 1000000 and -1000000 <= ry <= 1000000
                if not ok:
                    break
            if ok:
                engrave += 1

    return engrave
