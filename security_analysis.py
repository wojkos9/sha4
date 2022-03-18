from itertools import product, combinations
from utils import *
from keccak import sha3_256_enc
from utils import to_bits


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


def fun(b: list[int]) -> list[int]:
    pass


# def flip_bit(f, i):
#     return [f[j ^ 1<<i] for j in range(len(f))]

def flip_bit(bits, i):
    return [b ^ 1 if j == i else b for j, b in enumerate(bits)]

def hdist(f1, f2):
    return sum(x ^ y for (x, y) in zip(f1, f2))

def hamming(d1, d2):
    b1 = to_bits(d1)
    b2 = to_bits(d2)
    return hdist(b1, b2) / len(b1)

def sac_vals(bits):
    n = len(bits)
    m = len(bin(n)) - 2
    return [hamming(sha3_256_enc(bits), sha3_256_enc(flip_bit(bits, i))) for i in range(m)]

def test_sac():
    data = ["qwertyui", "asdfghj"][:1]
    for d in data:
        b = to_bits(d.encode('ascii'))
        v = sac_vals(b)
        print([v * 100 for v in v])

if __name__ == "__main__":
    test_sac()
