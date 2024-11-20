ZERO = 0j
UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1

def left_turn(heading):
    return heading * -1j

def right_turn(heading):
    return heading * 1j

def u_turn(heading):
    return heading * -1

def go_dist(from_pt, heading, dist):
    return from_pt + dist * heading

def as_xy(pt, t=float):
    return t(pt.real), t(pt.imag)

def from_xy(x, y):
    return x + 1j * y

def adj_ortho(pt, constrain_pos = None):
    adj = [pt + o for o in [-1, -1j, 1, 1j]]
    if constrain_pos is None:
        return adj
    return [a for a in adj if a in constrain_pos]

def adj_diag(pt, constrain_pos = None):
    adj = [pt + y + x for y in [-1j, 0, 1j] for x in [-1, 0, 1]]
    if constrain_pos is None:
        return adj
    return [a for a in adj if a in constrain_pos]

def m_dist(pt1, pt2 = ZERO):
    return abs(pt2.real - pt1.real) + abs(pt2.imag - pt1.imag)

def dist(pt1, pt2):
    return abs(pt2 - pt1)

def grid_as_dict(grid, valid = lambda x: True):
    res = {}
    for y, g in enumerate(grid):
        for x, c in enumerate(g):
            if valid(c):
                res[from_xy(x, y)] = c
    return res
