from itertools import combinations, pairwise
import math

from PIL import Image, ImageDraw

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    pattern = [int(x) for x in lines[0].split(',')]
    return pattern

CLEAR = (0, 0, 0, 0)
TRANS_YELLOW = (255, 255, 0, 64)
def draw_pattern(nails, pattern, fn, img_scale=700, chop=None):
    im_size = 2*(img_scale + 25)
    bg = Image.new('RGBA', (im_size, im_size), 'black')
    img = Image.new('RGBA', (im_size, im_size), 'black')
    draw = ImageDraw.Draw(img)
    pts = {}
    for th in range(1, nails + 1):
        x = img_scale * (1 + math.cos(2*math.pi/nails * (th - 1 - nails/4))) + 25
        y = img_scale * (1 + math.sin(2*math.pi/nails * (th - 1 - nails/4))) + 25
        pts[th] = (x, y)
        draw.ellipse((x-2, y-2, x+2, y+2), 'red')
    bg.alpha_composite(img)
    for a, b in pairwise(pattern):
        draw.rectangle((0, 0, im_size, im_size), CLEAR)
        draw.line([pts[a], pts[b]], TRANS_YELLOW)
        bg.alpha_composite(img)
    if chop:
        draw.line([pts[p] for p in chop], 'blue', 7)
        bg.alpha_composite(img)
    bg.save(fn)

def part1(output=False):
    pattern = parse('data/ec_2025/08-a.txt')
    nails = 32

    cnt = 0
    for p in pairwise(pattern):
        if max(p) - min(p) == nails // 2:
            cnt += 1

    if not output:
        return cnt

    draw_pattern(nails, pattern, fn:='ec_2025_08-a.png', 250)
    print(f'{fn} saved')
    return cnt

def intersect(s1, s2):
    if s1 == s2:
        return 1

    s1a, s1b = s1
    s2a, s2b = s2
    if s1a == s2a or s1a==s2b or s1b==s2a or s1b==s2b:
        return 0

    if s1b < s1a:
        s1a, s1b = s1b, s1a

    if s1a < s2a < s1b and not s1a < s2b < s1b:
        return 1

    if s1a < s2b < s1b and not s1a < s2a < s1b:
        return 1

    return 0

def part2(output=False):
    pattern = parse('data/ec_2025/08-b.txt')
    nails = 256

    knots = 0
    placed = []
    for s1 in pairwise(pattern):
        knots += sum(intersect(s1, s2) for s2 in placed)
        placed += [s1]

    if not output:
        return knots

    draw_pattern(nails, pattern, fn:='ec_2025_08-b.png')
    print(f'{fn} saved')
    return knots

def part3(output=False):
    pattern = parse('data/ec_2025/08-c.txt')
    nails = 256

    mc = 0
    the_chop = None
    for s1 in combinations(range(1, nails + 1), 2):
        cut = sum(intersect(s1, s2) for s2 in pairwise(pattern))
        if cut > mc:
            mc = cut
            the_chop = s1

    if not output:
        return mc

    draw_pattern(nails, pattern, fn:='ec_2025_08-c.png', chop = the_chop)
    print(f'{fn} saved')
    return mc
