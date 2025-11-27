from collections import defaultdict

from mrm.parse import all_nums

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    thicks = {}
    conns = {}
    cfgs = []
    curr_plant = None
    for l in lines:
        nums = list(all_nums(l))
        if l.startswith('Plant'):
            thicks[nums[0]] = nums[1]
            curr_plant = nums[0]
        elif 'free' in l:
            conns[(0, curr_plant)] = nums[0]
        elif 'branch' in l:
            conns[(nums[0], curr_plant)] = nums[1]
        elif '0' in l or '1' in l:
            cfgs += [nums]

    return thicks, conns, cfgs

def propagate_energy(thicks, conns, cfg=None):
    if cfg:
        cfg = iter(cfg)

    energy = {}
    for (c1, c2), tc in conns.items():
        if c1 == 0:
            if not cfg or next(cfg):
                energy[c2] = tc * thicks[c2]
            else:
                energy[c2] = 0

    while True:
        new_energy = defaultdict(int)
        for (c1, c2), tc in conns.items():
            if c2 in energy:
                continue
            if c1 not in energy:
                continue
            new_energy[c2] += energy[c1] * tc

        if len(new_energy) == 0:
            break

        for e in new_energy:
            if new_energy[e] >= thicks[e]:
                energy[e] = new_energy[e]
            else:
                energy[e] = 0

    return energy[max(thicks)]

def part1(output=False):
    thicks, conns, _ = parse('data/ec_2025/18-a.txt')

    energy = propagate_energy(thicks, conns)

    return energy

def part2(output=False):
    thicks, conns, cfgs = parse('data/ec_2025/18-b.txt')

    tot = 0
    for c in cfgs:
        energy = propagate_energy(thicks, conns, c)
        tot += energy
        if output:
            print(''.join(str(cv) for cv in c), energy)

    return tot

def part3(output=False):
    thicks, conns, cfgs = parse('data/ec_2025/18-c.txt')

    cfg_energy = [propagate_energy(thicks, conns, c) for c in cfgs]
    if output:
        print('Cases')
        for c, ce in zip(cfgs, cfg_energy):
            print(''.join(str(cv) for cv in c), ce)

    cfg_size = len(cfgs[0])
    max_cfg = [1] * cfg_size
    for (c1, _), tc in conns.items():
        if tc < 0:
            assert c1 <= cfg_size
            max_cfg[c1 - 1] = 0

    max_energy = propagate_energy(thicks, conns, max_cfg)
    if output:
        print()
        print('Maximal')
        print(''.join(str(cv) for cv in max_cfg), max_energy)

    return sum(max_energy - ce for ce in cfg_energy if ce)
