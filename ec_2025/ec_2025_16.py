from functools import partial

from mrm.search import fn_binary_search
from mrm.util import big_pi

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    return [int(x) for x in lines[0].split(',')]

def calc_blocks_used(spell, length):
    tot = 0
    for s in spell:
        tot += length // s

    return tot

def part1(output=False):
    spell = parse('data/ec_2025/16-a.txt')
    length = 90

    return calc_blocks_used(spell, length)

def spell_for_wall(wall):
    spell = []
    wall_len = len(wall)
    for i in range(1, 1 + wall_len):
        if wall[i - 1]:
            for j in range(i - 1, wall_len, i):
                wall[j] -= 1
            spell += [i]

    return spell

def part2(output=False):
    wall = parse('data/ec_2025/16-b.txt')

    return big_pi(spell_for_wall(wall))

def part3(output=False):
    wall = parse('data/ec_2025/16-c.txt')
    max_blocks = 202520252025000

    spell = spell_for_wall(wall)
    wall_len = fn_binary_search(partial(calc_blocks_used, spell), 1000, lambda x: x > max_blocks, output=output)

    return wall_len[0]
