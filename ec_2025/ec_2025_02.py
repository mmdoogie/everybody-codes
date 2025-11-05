import mrm.ansi_term as ansi
import mrm.cpoint as cpt
from mrm.parse import all_nums

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return cpt.from_xy(*all_nums(lines[0]))

def trunc_div(a, b):
    return cpt.from_xy(int(a.real / b.real), int(a.imag / b.imag))

def cycle(r, a, divisor):
    r = r * r
    r = trunc_div(r, divisor)
    r = r + a
    return r

def check_lim(r):
    return -1000000 <= r.real <= 1000000 and -1000000 <= r.imag <= 1000000

def part1(output=False):
    a = parse('data/ec_2025/02-a.txt')

    r = cpt.from_xy(0, 0)
    divisor = cpt.from_xy(10, 10)
    for _ in range(3):
        r = cycle(r, a, divisor)
    r = cpt.as_xy(r, int)

    return f'[{r[0]},{r[1]}]'

def part2(output=False):
    a = parse('data/ec_2025/02-b.txt')

    palette = [ansi.red, ansi.magenta, ansi.blue, ansi.cyan, ansi.green, ansi.yellow]

    engrave = 0
    divisor = cpt.from_xy(100000, 100000)
    for y in range(0, 1001, 10):
        for x in range(0, 1001, 10):
            r = cpt.from_xy(0, 0)
            p = cpt.from_xy(x, y) + a
            for i in range(100):
                r = cycle(r, p, divisor)
                ok = check_lim(r)
                if not ok:
                    break
            if output:
                print(palette[i//20]('**') if not ok else '  ', end='')
            if ok:
                engrave += 1
        if output:
            print()

    return engrave

def part3(output=False):
    a = parse('data/ec_2025/02-c.txt')

    engrave = 0
    divisor = cpt.from_xy(100000, 100000)
    for y in range(0, 1001, 1):
        for x in range(0, 1001, 1):
            r = cpt.from_xy(0, 0)
            p = cpt.from_xy(x, y) + a
            for _ in range(100):
                r = cycle(r, p, divisor)
                ok = check_lim(r)
                if not ok:
                    break
            if ok:
                engrave += 1

    return engrave
