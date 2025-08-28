def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def get_grid(lines):
    grid = {}
    for y, l in enumerate(lines):
        if '*' not in l:
            break
        for x, c in enumerate(l):
            grid[(x, y)] = c
    return grid, len(lines[0]), y

def get_tokens(lines):
    return [l for l in lines if 'R' in l or 'L' in l]

def score(in_slot, out_slot):
    tmp_score = 2 * out_slot - in_slot
    return max(tmp_score, 0)

def propagate(token, in_slot, grid, w, h):
    x = 2 * (in_slot - 1)
    y = -1

    for move in token:
        mx = 1 if move == 'R' else -1
        if x == 0 and mx == -1:
            mx = 1
        if x == w - 1 and mx == 1:
            mx = -1
        x = x + mx
        while y + 1 < h and grid[(x, y + 1)] == '.':
            y += 1
        if y >= h - 1:
            break
    return x // 2 + 1

def part1(output=False):
    lines = parse('data/ec_2/01-a.txt')
    grid, w, h = get_grid(lines)
    tokens = get_tokens(lines)
    tot_score = 0
    for x, t in enumerate(tokens):
        out_slot = propagate(t, x + 1, grid, w, h)
        sc = score(x + 1, out_slot)
        tot_score += sc
    return tot_score

def part2(output=False):
    lines = parse('data/ec_2/01-b.txt')
    grid, w, h = get_grid(lines)
    tokens = get_tokens(lines)
    tot_score = 0
    for t in tokens:
        max_score = 0
        for x in range(w // 2 + 1):
            out_slot = propagate(t, x + 1, grid, w, h)
            sc = score(x + 1, out_slot)
            max_score = max(sc, max_score)
        tot_score += max_score
    return tot_score

def part3(output=False):
    lines = parse('data/ec_2/01-c.txt')
    grid, w, h = get_grid(lines)
    tokens = get_tokens(lines)
    token_score = {}
    game_score_max = {}
    game_score_min = {}
    slots = w // 2 + 1
    for tn, t in enumerate(tokens):
        for x in range(slots):
            out_slot = propagate(t, x + 1, grid, w, h)
            sc = score(x + 1, out_slot)
            tokens_used = frozenset([tn])
            slots_used = frozenset([x])
            token_score[(tn, x)] = sc
            game_score_max[(tokens_used, slots_used)] = sc
            game_score_min[(tokens_used, slots_used)] = sc

    while True:
        add_game_score_min = {}
        add_game_score_max = {}
        for ptu, psu in game_score_min:
            for tn in range(len(tokens)):
                if tn in ptu:
                    continue
                ntu = ptu | set([tn])
                for sn in range(slots):
                    if sn in psu:
                        continue
                    nsu = psu | set([sn])
                    add_game_score_min[(ntu, nsu)] = min(add_game_score_min.get((ntu, nsu), 1000000), game_score_min[(ptu, psu)] + token_score[(tn, sn)])
                    add_game_score_max[(ntu, nsu)] = max(add_game_score_max.get((ntu, nsu), 0), game_score_max[(ptu, psu)] + token_score[(tn, sn)])
        if not add_game_score_min:
            break
        game_score_min = add_game_score_min
        game_score_max = add_game_score_max

    return f'{min(game_score_min.values())} {max(game_score_max.values())}'
