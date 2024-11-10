from itertools import combinations

def held_karp(points, weights, dont_loop = False, start_point = None, min_fn = min):
    n_pts = len(points)
    all_set = set(points)
    if start_point is not None:
        all_set.remove(start_point)
    else:
        start_point = all_set.pop()

    mets = {}
    pats = {}
    for set_size in range(1, n_pts):
        for subset in combinations(sorted(all_set), set_size):
            ss = set(list(subset))
            if set_size == n_pts - 1:
                if dont_loop:
                    return min_fn((mets[t := tuple(sorted(ss - set([si]))), si], pats[(t, si)]) for si in subset)
                min_sub = min_fn((mets[t := tuple(sorted(ss - set([si]))), si] + weights[(si, start_point)], pats[(t, si)]) for si in subset)
                return min_sub[0], min_sub[1] + (start_point,)
            for dest in all_set - ss:
                if set_size == 1:
                    mets[(subset, dest)] = weights[(start_point, subset[0])] + weights[(subset[0], dest)]
                    pats[(subset, dest)] = (start_point, subset[0], dest)
                else:
                    min_sub = min_fn((mets[t := tuple(sorted(ss - set([si]))), si] + weights[(si, dest)], pats[(t, si)]) for si in subset)
                    mets[(subset, dest)] = min_sub[0]
                    pats[(subset, dest)] = min_sub[1] + (dest,)

    return None
