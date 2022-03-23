from hashlib import sha3_256
from itertools import product, combinations
from utils import *
from keccak import sha3_256_enc
# from utils import to_bits
import random


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


def find_collision(hashes, bits, hash_f=sha3_256_enc):
    # random.seed(123)
    for hash in hashes[:1]:
        hash_bits = to_bits(hash)
        col = ""
        ctr = 0
        best = 0
        while True:
            data = random.randbytes(32)
            guess = hash_f(data)
            guess_bits = to_bits(guess)
            n = next(i for i in range(len(guess_bits)) if guess_bits[i] != hash_bits[i])
            best = max(best, n)
            print(n, 'best:', best)
            ctr += 1
            if n >= bits:
                break
        print('checked hashes:', ctr)
        print(hash_bits)
        print(guess_bits)


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
    n = 3 #len(bits)
    m = len(bin(n)) - 2
    base_hash = sha3_256_enc(bits)
    return [hamming(base_hash, sha3_256_enc(flip_bit(bits, i))) for i in range(n)]

# 49.603271484375
def test_sac():
    data = ["qwertyui", "asdfghj"][:1]
    for d in data:
        b = to_bits(d.encode('ascii'))
        v = sac_vals(b)
        print([v * 100 for v in v])

def test_balance1(bits: list[int]):
    return bits.count(1) / len(bits)

def test_balance(n=5):
    random.seed(1337)
    data = [random.randbytes(32) for _ in range(n)]
    c = 0
    for d in data:
        h = sha3_256_enc(d)
        bal = test_balance1(to_bits(h))
        print(bal, d, h)
        c += bal
    print(c / n)

def test_distribution(n=4, hash_f=sha3_256_enc):
    counts = [0] * 2**n
    for _ in range(1000):
        r = random.randbytes(32)
        h = hash_f(r)
        b = from_bits1(to_bits(h)[:n])
        print(b)
        counts[b] += 1
        print(counts)

if __name__ == "__main__":
    test_distribution(hash_f=lambda d: sha3_256(d).digest())