from collections import defaultdict
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
    if s1[0] == s2[1] and s1[1] == s2[0]:
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

    fwd_from_node = defaultdict(list)
    fwd_to_node = defaultdict(list)
    for a, b in pairwise(pattern):
        fwd_from_node[min(a, b)] += [max(a, b)]
        fwd_to_node[max(a, b)] += [min(a, b)]

    max_cut = 0
    the_chop = None
    for ca, cb in combinations(range(1, nails + 1), 2):
        # Don't care about circle edges
        if cb - ca == 1:
            continue

        # Start from fresh set when we have a new gap
        # All paths to/from the gap node that are not directly adjacent will intersect
        if cb - ca == 2:
            active = defaultdict(int)
            for dest in fwd_from_node[cb - 1]:
                if dest != cb:
                    active[dest] += 1
            for src in fwd_to_node[cb - 1]:
                if src < ca:
                    active[src] += 1
        else:
            # Otherwise, expand/contract by only the possible changes from moving the end by one node
            # Any path that touches the end node can no longer intersect
            if cb in active:
                active[cb] = 0
            # Then add the paths from the most recently exposed node
            for dest in fwd_from_node[cb - 1]:
                if dest != cb:
                    active[dest] += 1
            for src in fwd_to_node[cb - 1]:
                if src < ca:
                    active[src] += 1

        # If the current chop coincides with paths, we need to count those for only this round
        coincide = 0
        for dest in fwd_from_node[ca]:
            if dest == cb:
                coincide += 1
        cut = sum(active.values()) + coincide

        if cut > max_cut:
            max_cut = cut
            the_chop = (ca, cb)

    if not output:
        return max_cut

    draw_pattern(nails, pattern, fn:='ec_2025_08-c.png', chop = the_chop)
    print(f'{fn} saved')
    return max_cut
