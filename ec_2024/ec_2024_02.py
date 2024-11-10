import re

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip() for l in f.readlines()]
    words = lines[0].split(':')[1].split(',')
    return words, lines[2:]

def part1(output):
    words, lines = parse('data/ec_2024/02-a.txt')

    tot = 0
    for l in lines:
        for w in words:
            m = re.findall(f'(?=({w}))', l)
            tot += len(m)
    return tot

def find_hits(word, line, hits, wrap=False, bidir=True, output=False):
    n = len(line)
    if wrap:
        line = line + line

    m = re.finditer(f'(?=({word}))', line)
    for mm in m:
        if mm.start(1) >= n:
            continue
        hits = hits[:mm.start(1)] + 'x' * (mm.end(1) - mm.start(1)) + hits[mm.end(1):]
        if mm.end(1) >= n:
            w = mm.end(1) - n
            hits = hits[-w:] + hits[w:-w]
        if output:
            print(hits, mm.group(1), '@', mm.span(1))

    if not bidir or word[::1] == word[::-1]:
        return hits

    m = re.finditer(f'(?=({word[::-1]}))', line)
    for mm in m:
        if mm.start(1) >= n:
            continue
        hits = hits[:mm.start(1)] + 'x' * (mm.end(1) - mm.start(1)) + hits[mm.end(1):]
        if mm.end(1) >= n:
            w = mm.end(1) - n
            hits = hits[-w:] + hits[w:-w]
        if output:
            print(hits, mm.group(1), '@', mm.span(1))

    return hits

def part2(output):
    words, lines = parse('data/ec_2024/02-b.txt')

    hits = ['_' * len(l) for l in lines]
    for i, l in enumerate(lines):
        if output:
            print()
            print(l)

        for w in words:
            hits[i] = find_hits(w, l, hits[i], wrap=False, bidir=True, output=output)

    return sum(c == 'x' for h in hits for c in h)

def transp(txt):
    return [''.join(txt[r][c] for r in range(len(txt))) for c in range(len(txt[0]))]

def part3(output):
    words, lines = parse('data/ec_2024/02-c.txt')

    hits = ['_' * len(l) for l in lines]
    for i, l in enumerate(lines):
        if output:
            print()
            print(l)

        for w in words:
            hits[i] = find_hits(w, l, hits[i], wrap=True, bidir=True, output=output)

    hits = transp(hits)
    lines = transp(lines)

    for i, l in enumerate(lines):
        if output:
            print()
            print(l)

        for w in words:
            hits[i] = find_hits(w, l, hits[i], wrap=False, bidir=True, output=output)

    return sum(c == 'x' for h in hits for c in h)
