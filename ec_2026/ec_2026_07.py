from collections import defaultdict

from mrm.parse import all_nums

def parse(fn):
    with open(fn, 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    energy = {}
    conns = {}

    for l in lines:
        nums = list(all_nums(l))
        src = nums[0]
        energy[src] = nums[1]
        conns[src] = nums[2:]

    return energy, conns

def part1(output=False):
    energy, conns = parse('data/ec_2026/07-a.txt')
    start = max((len(v), k) for k, v in conns.items())[1]

    if output:
        print('Start:', start)
        print('Energy', sum(energy.values()))

    propset = set([start])
    for imp in range(5, 0, -1):
        newprop = []
        for p in propset:
            energy[p] += imp
            newprop += conns[p]
        propset = newprop
        if output:
            print('\nImpulse:', imp)
            print('Energy', sum(energy.values()))
            if imp != 1:
                print('Propagating to:', propset)

    return sum(energy.values())

def part2(output=False):
    energy, conns = parse('data/ec_2026/07-b.txt')
    start = max((len(v), k) for k, v in conns.items())[1]

    if output:
        print('Start:', start)
        print('Energy', sum(energy.values()))

    propset = {start: 1}
    for imp in range(10, 0, -1):
        newprop = defaultdict(int)
        for k, v in propset.items():
            energy[k] += v * imp
            for c in conns[k]:
                newprop[c] += propset[k]
        propset = newprop
        if output:
            print('\nImpulse:', imp)
            print('Energy', sum(energy.values()))
            if imp != 1:
                print('Propagating to:', propset)


    return sum(energy.values())

def part3(output=False):
    base_energy, conns = parse('data/ec_2026/07-c.txt')

    max_energy = 0
    for start in base_energy:
        if output:
            print('\nTrying from:', start)

        energy = dict(base_energy.items())

        all_propsets = [{start: 1}]
        all_imps = [10]

        exploded = set()
        while True:
            new_all_propsets = []
            new_all_imps = []
            for propset, imp in zip(all_propsets, all_imps):
                new_propset = defaultdict(int)
                for p in propset:
                    if p in exploded:
                        continue
                    energy[p] += propset[p] * imp
                    for c in conns[p]:
                        new_propset[c] += propset[p]
                if imp > 1 and new_propset:
                    new_all_propsets += [new_propset]
                    new_all_imps += [imp - 1]
            all_propsets = new_all_propsets
            all_imps = new_all_imps

            for e in energy:
                if e in exploded:
                    continue
                if energy[e] >= 1000000:
                    exploded.add(e)
                    all_propsets += [{c: 1 for c in conns[e]}]
                    all_imps += [10]

            total = sum(v for k, v in energy.items() if k not in exploded)
            if output:
                print(f'Impulses: {len(all_imps):3d} -- Energy: {total: 10d} -- Exploded: {len(exploded):3d}')

            if not all_imps or total == 0:
                break

        if total > max_energy:
            max_energy = total

    return max_energy
