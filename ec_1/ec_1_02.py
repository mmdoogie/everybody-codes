from collections import Counter
import re

from mrm.parse import all_nums

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    pat = re.compile(r'ADD id=([0-9]+) left=\[([0-9]+),([A-Z!]+)\] right=\[([0-9]+),([A-Z!]+)\]')
    mat = [pat.match(l).groups() if 'ADD' in l else [next(all_nums(l)), -1, -1, -1, -1] for l in lines]
    return [(int(a), int(b), c, int(d), e) for a, b, c, d, e in mat]

class Node:
    def __init__(self, rank, sym):
        self.rank = rank
        self.sym = sym
        self.left = None
        self.right = None
        self.parent = None
        self.root = None
        self.level = 0
        self.path = ''
    def __repr__(self):
        return f'<< {self.rank} {self.sym} {self.level} {self.path} >>'

def clean_tree(node, root, lev, pat):
    if not node:
        return
    node.level = lev
    node.path = pat
    node.root = root
    clean_tree(node.left, root, node.level + 1, node.path + 'L')
    clean_tree(node.right, root, node.level + 1, node.path + 'R')

def tree_insert(root, node):
    at = root
    while True:
        if node.rank < at.rank:
            if at.left:
                at = at.left
                continue
            at.left = node
            node.level = at.level + 1
            node.path = at.path + 'L'
            node.parent = at
            node.root = root
            return
        else:
            if at.right:
                at = at.right
                continue
            at.right = node
            node.level = at.level + 1
            node.path = at.path + 'R'
            node.parent = at
            node.root = root
            return

def part1(output=False):
    lines = parse('data/ec_1/02-a.txt')
    left = None
    right = None
    allnodes = []

    for l in lines:
        _, lrank, lsym, rrank, rsym = l

        lnode = Node(lrank, lsym)
        if left:
            tree_insert(left, lnode)
        else:
            left = lnode

        rnode = Node(rrank, rsym)
        if right:
            tree_insert(right, rnode)
        else:
            right = rnode

        allnodes += [lnode, rnode]

    res = ''
    for root in [left, right]:
        level_cnt = Counter(n.level for n in allnodes if n.root == root)
        select_level = level_cnt.most_common(1)[0][0]
        select_nodes = [n for n in allnodes if n.level == select_level and n.root == root]
        res += ''.join(n.sym for n in sorted(select_nodes, key=lambda x: x.rank))
    return res

def part2(output=False):
    lines = parse('data/ec_1/02-b.txt')
    left = None
    right = None
    allnodes = {}

    for l in lines:
        lid, lrank, lsym, rrank, rsym = l

        if lrank == -1:
            lnode, rnode = allnodes[lid]
            lnode.rank, rnode.rank = rnode.rank, lnode.rank
            lnode.sym, rnode.sym = rnode.sym, lnode.sym
            continue

        lnode = Node(lrank, lsym)
        if left:
            tree_insert(left, lnode)
        else:
            left = lnode

        rnode = Node(rrank, rsym)
        if right:
            tree_insert(right, rnode)
        else:
            right = rnode

        allnodes[lid] = [lnode, rnode]

    res = ''
    for side in range(2):
        level_cnt = Counter(n[side].level for n in allnodes.values())
        select_level = level_cnt.most_common(1)[0][0]
        select_nodes = [n[side] for n in allnodes.values() if n[side].level == select_level]
        res += ''.join(n.sym for n in sorted(select_nodes, key=lambda x: x.path))
    return res

def part3(output=False):
    lines = parse('data/ec_1/02-c.txt')
    left = None
    right = None
    allnodes = {}

    for l in lines:
        lid, lrank, lsym, rrank, rsym = l

        if lrank == -1:
            n1, n2 = allnodes[lid]
            if lid == 1:
                left, right = right, left
                continue

            if n1.parent.left == n1:
                n1.parent.left = n2
            else:
                n1.parent.right = n2

            if n2.parent.left == n2:
                n2.parent.left = n1
            else:
                n2.parent.right = n1

            n1.parent, n2.parent = n2.parent, n1.parent

            clean_tree(left, left, 0, '')
            clean_tree(right, right, 0, '')
            continue

        lnode = Node(lrank, lsym)
        if left:
            tree_insert(left, lnode)
        else:
            left = lnode

        rnode = Node(rrank, rsym)
        if right:
            tree_insert(right, rnode)
        else:
            right = rnode

        allnodes[lid] = [lnode, rnode]

    res = ''
    for root in [left, right]:
        level_cnt = Counter(n.level for anv in allnodes.values() for n in anv if n.root == root)
        select_level = level_cnt.most_common(1)[0][0]
        select_nodes = [n for anv in allnodes.values() for n in anv if n.level == select_level and n.root == root]
        res += ''.join(n.sym for n in sorted(select_nodes, key=lambda x: x.path))
    return res
