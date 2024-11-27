def prim_mst(ngh, wts, start_point=None):
    in_set = set()
    out_set = set(ngh)
    edges = []
    if start_point is None:
        start_point = out_set.pop()
    else:
        if len(ngh.get(start_point, [])) != 0:
            out_set.remove(start_point)
    in_set.add(start_point)
    while out_set:
        rem_dists = [(wts[pair := (a, b)], pair) for a in in_set for b in ngh[a] if b not in in_set]
        if len(rem_dists) == 0:
            return in_set, edges
        choose = min(rem_dists)[1]
        edges += [choose]
        in_set.add(choose[1])
        out_set.remove(choose[1])
    return in_set, edges
