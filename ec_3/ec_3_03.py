from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Node:
    node_id: int
    plug_shape: str
    left_shape: str
    right_shape: str
    data: str
    left: Optional['Node'] = field(default=None)
    right: Optional['Node'] = field(default=None)

    def __repr__(self):
        return f"@{self.node_id} P:{self.plug_shape} L:{self.left_shape} #{self.left.node_id if self.left else '-'} R:{self.right_shape} #{self.right.node_id if self.right else '-'}"

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    nodes = []
    for l in lines:
        parts = l.split(', ')
        node_id = int(parts[0].split('=')[1])
        shapes = [a.split('=')[1] for a in parts[1:]]
        nodes += [Node(node_id, *shapes)]
    return nodes

def bfs_ins(at: Node, nn: Node, match=lambda a, b: a == b, replace_weak=False):
    if not at.left and match(at.left_shape, nn.plug_shape):
        at.left = nn
        return True, None
    if at.left:
        if replace_weak and at.left_shape != at.left.plug_shape and at.left_shape == nn.plug_shape:
            nn, at.left = at.left, nn
        else:
            did, nn = bfs_ins(at.left, nn, match, replace_weak)
            if did:
                return True, None
    if not at.right and match(at.right_shape, nn.plug_shape):
        at.right = nn
        return True, None
    if at.right:
        if replace_weak and at.right_shape != at.right.plug_shape and at.right_shape == nn.plug_shape:
            nn, at.right = at.right, nn
        else:
            did, nn = bfs_ins(at.right, nn, match, replace_weak)
            if did:
                return True, None
    return False, nn

def bfs_read(at: Node, order=None):
    if order is None:
        order = []
    if at.left:
        bfs_read(at.left, order)
    order += [at.node_id]
    if at.right:
        bfs_read(at.right, order)
    return order

def part1(output=False):
    nodes = parse('data/ec_3/03-a.txt')

    tree = nodes[0]
    for n in nodes[1:]:
        did_ins, _ = bfs_ins(tree, n)
        assert did_ins

    order = bfs_read(tree)
    return sum((pos + 1) * node_id for pos, node_id in enumerate(order))

def partial_match(a, b):
    if a == b:
        return True
    a1, a2 = a.split(' ')
    b1, b2 = b.split(' ')
    return a1 == b1 or a2 == b2

def part2(output=False):
    nodes = parse('data/ec_3/03-b.txt')

    tree = nodes[0]
    for n in nodes[1:]:
        did_ins, _ = bfs_ins(tree, n, partial_match)
        assert did_ins

    order = bfs_read(tree)
    return sum((pos + 1) * node_id for pos, node_id in enumerate(order))

def part3(output=False):
    nodes = parse('data/ec_3/03-c.txt')

    tree = nodes[0]

    for n in nodes[1:]:
        did_ins, wrap_node = bfs_ins(tree, n, partial_match, replace_weak=True)
        assert did_ins or wrap_node != n
        if not did_ins:
            did_ins, _ = bfs_ins(tree, wrap_node, partial_match, replace_weak = True)
        assert did_ins

    order = bfs_read(tree)
    return sum((pos + 1) * node_id for pos, node_id in enumerate(order))
