from mrm.graph import all_components
import mrm.image as img
import mrm.point as pt

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid = pt.grid_as_dict(lines, valid=lambda x: x == '#')
    adj = {g: pt.adj_ortho(g, grid) for g in grid}
    cmps = all_components(adj)
    return cmps

def part1(output=False):
    cmps = parse('data/ec_2026/12-a.txt')

    spells = 0
    for cmp in cmps:
        x1, x2 = img.minmax_x(cmp)
        y1, y2 = img.minmax_y(cmp)
        width  = x2 - x1 + 1
        height = y2 - y1 + 1
        spells += min(width, height)

        if output:
            img.print_image(cmp, highlighter=lambda x, y, c: '#' if (x, y) in cmp else ' ')
            print(f'Size: {width} x {height}, Spells: {min(width, height)}')

    return spells

def score_by_rows(cmp):
    x1, x2 = img.minmax_x(cmp)
    y1, y2 = img.minmax_y(cmp)
    main_width = x2 - x1 + 1
    main_height = 0
    sub_width = 0
    sub_height = 0
    for y in range(y1, y2 + 1):
        if (x1, y) in cmp and (x2, y) in cmp:
            main_height += 1
        else:
            sub_height += 1
            if not sub_width:
                xs = [cx for cx, cy in cmp if cy == y]
                sub_width = max(xs) - min(xs) + 1
    return min(main_width, main_height) + min(sub_width, sub_height), sub_height

def score_by_cols(cmp):
    x1, x2 = img.minmax_x(cmp)
    y1, y2 = img.minmax_y(cmp)
    main_width = 0
    main_height = y2 - y1 + 1
    sub_width = 0
    sub_height = 0
    for x in range(x1, x2 + 1):
        if (x, y1) in cmp and (x, y2) in cmp:
            main_width += 1
        else:
            sub_width += 1
            if not sub_height:
                ys = [cy for cx, cy in cmp if cx == x]
                sub_height = max(ys) - min(ys) + 1
    return min(main_width, main_height) + min(sub_width, sub_height)

def part2(output=False):
    cmps = parse('data/ec_2026/12-b.txt')

    spells = 0
    for cmp in cmps:
        x1, x2 = img.minmax_x(cmp)
        y1, y2 = img.minmax_y(cmp)
        width  = x2 - x1 + 1
        height = y2 - y1 + 1
        if len(cmp) == width * height:
            spells += min(width, height)
        elif len(cmp) == width + height - 1:
            spells += 2
        else:
            base_score = min(width, height)
            row_score, _ = score_by_rows(cmp)
            col_score = score_by_cols(cmp)
            spells += min(base_score, row_score, col_score)

            if output:
                img.print_image(cmp, highlighter=lambda x, y, c: '#' if (x, y) in cmp else ' ')
                print(f'Base: {base_score}, By Rows: {row_score}, By Cols: {col_score}')

    return spells

def score_by_rows_with_gap(cmp):
    x1, x2 = img.minmax_x(cmp)
    y1, y2 = img.minmax_y(cmp)
    main_width = x2 - x1 + 1
    sub_width_1 = 0
    sub_width_2 = 0
    sub_height = 0
    spells = 0
    for y in range(y1, y2 + 1):
        xs = [cx for cx, cy in cmp if cy == y]
        if len(xs) == main_width:
            spells += 1
            continue
        if not sub_width_1:
            lefts  = sorted([x for x in xs if x - 1 not in xs])
            rights = sorted([x for x in xs if x + 1 not in xs])
            sub_width_1 = rights[0] - lefts[0] + 1
            sub_width_2 = rights[1] - lefts[1] + 1
        sub_height += 1
    spells += min(sub_width_1, sub_height) + min(sub_width_2, sub_height)
    return spells

def score_by_cols_with_gap(cmp):
    x1, x2 = img.minmax_x(cmp)
    y1, y2 = img.minmax_y(cmp)
    main_height = y2 - y1 + 1
    sub_height_1 = 0
    sub_height_2 = 0
    sub_width = 0
    spells = 0
    for x in range(x1, x2 + 1):
        ys = [cy for cx, cy in cmp if cx == x]
        if len(ys) == main_height:
            spells += 1
            continue
        if not sub_height_1:
            tops = sorted([y for y in ys if y - 1 not in ys])
            bots = sorted([y for y in ys if y + 1 not in ys])
            sub_height_1 = bots[0] - tops[0] + 1
            sub_height_2 = bots[1] - tops[1] + 1
        sub_width += 1
    spells += min(sub_height_1, sub_width) + min(sub_height_2, sub_width)
    return spells

def part3(output=False):
    cmps = parse('data/ec_2026/12-c.txt')

    spells = 0
    for cmp in cmps:
        x1, x2 = img.minmax_x(cmp)
        y1, y2 = img.minmax_y(cmp)
        width  = x2 - x1 + 1
        height = y2 - y1 + 1
        row_score, sub_height = score_by_rows(cmp)
        if len(cmp) == width * height:
            spells += min(width, height)
        elif len(cmp) == width + height - 1:
            spells += 2
        elif sub_height:
            base_score = min(width, height)
            col_score = score_by_cols(cmp)
            spells += min(base_score, row_score, col_score)
        else:
            row_score = score_by_rows_with_gap(cmp)
            col_score = score_by_cols_with_gap(cmp)
            spells += min(row_score, col_score)

            if output:
                img.print_image(cmp, highlighter=lambda x, y, c: '#' if (x, y) in cmp else ' ')
                print(f'By Rows: {row_score}, By Cols: {col_score}')

    return spells
