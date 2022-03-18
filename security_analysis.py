from itertools import product, combinations
from utils import *


def check_nonlinearity(hashes):
    all_f = [list(p) for p in product([0, 1], repeat=8)]
    tab_res = []

    for f in all_f:
        rf = []
        for x in all_f:
            r = 0
            for a, b in zip(x, f):
                r = r ^ (a * b)
            rf += [r]
        tab_res.append(rf)

    tab_res2 = []

    for r in tab_res:
        res = [1 ^ rr for rr in r]
        tab_res2.append(res)

    all_res = tab_res + tab_res2
    func = []
    for h in hashes:
        func.append(to_bits(h))

    for i, f in enumerate(func):
        sums = []
        for r in all_res:
            s = sum([ff ^ rr for ff, rr in zip(f, r)])
            sums.append(s)
        print(f"{hashes[i]}: {min(sums)}")
