from functools import cache, partial
from itertools import count

import mrm.ansi_term as ansi
import mrm.image as img
import mrm.point as pt

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid = pt.grid_as_dict(lines)
    active = set(gl for gl, gc in grid.items() if gc == '#')
    inactive = set(grid) - active
    return grid, active, inactive

def active_ch(active, grid, x, y, _, p3_active=None, p3_inactive=None):
    p = (x, y)
    if p in active:
        if p3_active and p in p3_active:
            return ansi.blue('#')
        return '#'
    if p in grid:
        if p3_inactive and p in p3_inactive:
            return ansi.blue('.')
        return '.'
    return ' '

def sim_and_cnt(grid, active, rounds, output):
    if output:
        ansi.clear_screen()
        img.print_image(grid, True, highlighter=partial(active_ch, active, grid))
        print('  Round 0')
        print()

    @cache
    def ngh(g):
        return set(pt.adj_diag(g, grid)) - set(pt.adj_ortho(g, grid))

    cnt = 0
    for rnd in range(rounds):
        next_active = set()
        for g in grid:
            even = sum(1 for n in ngh(g) if n in active) % 2 == 0
            if g in active and not even:
                next_active.add(g)
            if g not in active and even:
                next_active.add(g)
        active = next_active
        cnt += len(active)

        if output:
            with ansi.hidden_cursor():
                ansi.cursor_home()
                img.print_image(grid, True, highlighter=partial(active_ch, active, grid))
                print(f'  Round {rnd + 1}')
                print()

    return cnt

def part1(output=False):
    grid, active, _ = parse('data/ec_2025/14-a.txt')
    return sim_and_cnt(grid, active, 10, output)

def part2(output=False):
    grid, active, _ = parse('data/ec_2025/14-b.txt')
    return sim_and_cnt(grid, active, 2025, output)

def find_loop(match_active, match_inactive, output):
    grid = {(x, y) for y in range(34) for x in range(34)}
    active = set()
    counts = {}
    patterns = {}

    @cache
    def ngh(g):
        return set(pt.adj_diag(g, grid)) - set(pt.adj_ortho(g, grid))

    for rnd in count():
        next_active = set()
        for g in grid:
            even = sum(1 for n in ngh(g) if n in active) % 2 == 0
            if g in active and not even:
                next_active.add(g)
            if g not in active and even:
                next_active.add(g)
        active = next_active
        if all(m in active for m in match_active) and all(m not in active for m in match_inactive):
            done = False
            for pat_rnd, pat in patterns.items():
                if pat == active:
                    repeat_src = rnd
                    repeat_dst = pat_rnd
                    done = True
                    break
            counts[rnd] = len(active)
            patterns[rnd] = active
            if output:
                with ansi.saved_cursor():
                    img.print_image(grid, False, highlighter=partial(active_ch, active, grid, p3_active=match_active, p3_inactive=match_inactive))
                    print(f'Pattern match at round {rnd + 1}')
                    print()
            if done:
                break
    if output:
        ansi.clear_screen()
        print(f'Loop detected from round {repeat_src} to {repeat_dst}')
        print(f'Patterns matched at rounds {list(counts.keys())}')

    return repeat_src, repeat_dst, counts

def calc_active(rounds, repeat_src, repeat_dst, counts, output):
    rem_rnds = rounds - repeat_dst
    tot = sum(cv for ck, cv in counts.items() if ck <= repeat_dst)

    if output:
        print( 'Rounds to calculate:               1000000000')
        print(f'Rounds remaining at start of loop:  {rem_rnds}')
        print(f'Active cells at start of loop:      {tot}')

    repeat_len = repeat_src - repeat_dst
    full_repeats = rem_rnds // repeat_len
    repeat_cnt = sum(cv for ck, cv in counts.items() if repeat_dst < ck <= repeat_src)
    rem_rnds -= full_repeats * repeat_len
    tot += full_repeats * repeat_cnt

    if output:
        print(f'Loop length:                        {repeat_len}')
        print(f'Complete repeats:                   {full_repeats}')
        print(f'Active cells per full loop:         {repeat_cnt}')
        print(f'Rounds remaining after full loops:  {rem_rnds}')
        print(f'Active cells after full loops:      {tot}')

    repeat_cnt = sum(cv for ck, cv in counts.items() if repeat_dst < ck <= rem_rnds + repeat_dst)
    tot += repeat_cnt

    if output:
        print(f'Active cells from partial loop:     {repeat_cnt}')
        print(f'Active cells:                       {tot}')

    return tot

def part3(output=False):
    match_grid, match_active, match_inactive = parse('data/ec_2025/14-c.txt')

    if output:
        ansi.clear_screen()
        img.print_image(match_grid, True, highlighter=partial(active_ch, match_active, match_grid))
        print('Match Pattern')

    m_w, m_h = img.max_xy(match_grid)
    match_active = {(x + 16 - m_w // 2, y + 16 - m_h // 2) for x, y in match_active}
    match_inactive = {(x + 16 - m_w // 2, y + 16 - m_h // 2) for x, y in match_inactive}

    repeat_src, repeat_dst, counts = find_loop(match_active, match_inactive, output)

    return calc_active(1000000000, repeat_src, repeat_dst, counts, output)
