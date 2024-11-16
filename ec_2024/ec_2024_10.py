from mrm.iter import batched

def file_lines(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip() for l in f.readlines()]
    return lines

def resolve_basic(grid):
    for y, line in enumerate(grid):
        for x, ch in enumerate(line):
            if ch != '.':
                continue
            row = set(line).difference('.')
            col = set(row[x] for row in grid).difference('.')
            match = row.intersection(col)
            if len(match) == 0 and '?' not in row and '?' not in col:
                return False
            if len(match) != 0:
                grid[y] = grid[y][:x] + match.pop() + grid[y][x+1:]
    return True

def get_runeword(grid):
    return ''.join(grid[y][2:6] for y in range(2,6))

def part1(output):
    lines = file_lines('data/ec_2024/10-a.txt')
    resolve_basic(lines)
    return get_runeword(lines)

def score_runeword(runeword):
    if '.' in runeword:
        return 0
    return sum((ord(c) - ord('A') + 1) * (i + 1) for i, c in enumerate(runeword))

def part2(output):
    lines = file_lines('data/ec_2024/10-b.txt')
    tot = 0
    for row_of_grids in batched(lines, 9):
        if row_of_grids[-1] == '':
            row_of_grids = row_of_grids[:-1]
        split_lines = [l.split(' ') for l in row_of_grids]
        for one_grid in zip(*split_lines):
            grid = list(one_grid)
            resolve_basic(grid)
            tot += score_runeword(get_runeword(grid))
    return tot

def resolve_advanced(grid):
    for y, line in enumerate(grid):
        for x, ch in enumerate(line):
            if ch != '.':
                continue
            row_set = list(set(line).difference('.'))
            col_set = list(set(row[x] for row in grid).difference('.'))
            row_cnt = [sum(ch == r for ch in line) for r in row_set]
            col_cnt = [sum(row[x] == c for row in grid) for c in col_set]
            if '?' in col_set and '?' not in row_set:
                sum_1 = sum(s == 1 for s in row_cnt)
                sum_2 = sum(s == 2 for s in row_cnt)
                if sum_1 != 1 or sum_2 != 3:
                    continue
                letter = row_set[row_cnt.index(1)]
                if letter == '?':
                    continue
                grid[y] = grid[y][:x] + letter + grid[y][x+1:]
            elif '?' in row_set and '?' not in col_set:
                sum_1 = sum(s == 1 for s in col_cnt)
                sum_2 = sum(s == 2 for s in col_cnt)
                if sum_1 != 1 or sum_2 != 3:
                    continue
                letter = col_set[col_cnt.index(1)]
                if letter == '?':
                    continue
                grid[y] = grid[y][:x] + letter + grid[y][x+1:]

def resolve_question_marks(grid):
    for y, line in enumerate(grid):
        for x, ch in enumerate(line):
            if ch != '?':
                continue
            row_set = list(set(line).difference('.?'))
            col_set = list(set(row[x] for row in grid).difference('.?'))
            row_cnt = [sum(ch == r for ch in line) for r in row_set]
            col_cnt = [sum(row[x] == c for row in grid) for c in col_set]
            if '*' in col_set:
                sum_1 = sum(s == 1 for s in row_cnt)
                sum_2 = sum(s == 2 for s in row_cnt)
                if sum_1 != 1 or sum_2 != 3:
                    continue
                letter = row_set[row_cnt.index(1)]
                grid[y] = grid[y][:x] + letter + grid[y][x+1:]
            elif '*' in row_set:
                sum_1 = sum(s == 1 for s in col_cnt)
                sum_2 = sum(s == 2 for s in col_cnt)
                if sum_1 != 1 or sum_2 != 3:
                    continue
                letter = col_set[col_cnt.index(1)]
                if letter == '?':
                    continue
                grid[y] = grid[y][:x] + letter + grid[y][x+1:]

def propagate_question_marks(subgrids, xcnt, ycnt):
    for (sgx, sgy), grid in subgrids.items():
        if all('?' not in line for line in grid):
            continue
        for y, line in enumerate(grid):
            if '?' not in line:
                continue
            for x, ch in enumerate(line):
                if ch != '?':
                    continue
                ogl = '?'
                if y < 2 and sgy > 0:
                    ogl = subgrids[(sgx, sgy - 1)][-2 + y][x]
                if y > 5 and sgy < ycnt - 1:
                    ogl = subgrids[(sgx, sgy + 1)][y - 6][x]
                if x < 2 and sgx > 0:
                    ogl = subgrids[(sgx - 1, sgy)][y][-2 + x]
                if x > 5 and sgx < xcnt - 1:
                    ogl = subgrids[(sgx + 1, sgy)][y][x - 6]
                if ogl != '?':
                    grid[y] = grid[y][:x] + ogl + grid[y][x + 1:]

def part3(output):
    lines = file_lines('data/ec_2024/10-c.txt')

    width = len(lines[0])
    height = len(lines)
    x_cnt = (width - 2) // 6
    y_cnt = (height - 2) // 6

    subgrids = {}
    for y in range(y_cnt):
        for x in range(x_cnt):
            subgrid = [r[x * 6:(x + 1) * 6 + 2] for r in lines[y * 6:(y + 1) * 6 + 2]]
            subgrids[(x,y)] = subgrid

    done_cnt = 0
    prev_done_cnt = -1
    while done_cnt > prev_done_cnt:
        prev_done_cnt = done_cnt

        propagate_question_marks(subgrids, x_cnt, y_cnt)

        for s in subgrids.values():
            resolve_basic(s)
            resolve_advanced(s)
            resolve_question_marks(s)

        done_cnt = sum('.' not in get_runeword(s) for s in subgrids.values())

    return sum(score_runeword(get_runeword(s)) for s in subgrids.values())
