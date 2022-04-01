from hashlib import sha3_256
from itertools import product, combinations
from utils import *
from keccak import sha3_256_enc
import random
# import pandas as pd
import matplotlib.pyplot as plt


def check_nonlinearity(hashes):
    all_f = [list(p) for p in product([0, 1], repeat=8)]
    tab_res = []
    sums_res = []

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
        sums_res.append(min(sums))

    return sums_res


def get_nonlinearity_chart(data1, data2):
    data = {'Input': data1,
            'Hashes': data2}

    df = pd.DataFrame(data)
    df.plot(x='Input', y='Hashes', kind='scatter', ylim=(0, max(data2) + 10))
    plt.show()


def find_collision(niter, bits, hash_f=sha3_256_enc):
    # random.seed(123)
    cum = 0
    for j in range(niter):
        hash = hash_f(random.randbytes(32))
        hash_bits = to_bits(hash)
        ctr = 0
        best = 0
        while True:
            data = random.randbytes(32)
            guess = hash_f(data)
            guess_bits = to_bits(guess)
            m = next(i for i in range(len(guess_bits)) if guess_bits[i] != hash_bits[i])
            best = max(best, m)
            print(j, m, 'best:', best)
            ctr += 1
            if m >= bits:
                break
        cum += ctr
    r = cum / niter
    print(niter, bits, ':', r)
    return r
        # print('checked hashes:', ctr)
        # print(hash_bits)
        # print(guess_bits)



def flip_bit(bits, i):
    return [b ^ 1 if j == i else b for j, b in enumerate(bits)]


def hdist(f1, f2):
    return sum(x ^ y for (x, y) in zip(f1, f2))


def hamming(d1, d2):
    b1 = to_bits(d1)
    b2 = to_bits(d2)
    return hdist(b1, b2) / len(b1)


def sac_vals(bits):
    n = 16 # len(bits)
    # m = len(bin(n)) - 2
    base_hash = sha3_256_enc(bits)
    return [hamming(base_hash, sha3_256_enc(flip_bit(bits, i))) for i in range(n)]


# 49.603271484375
def test_sac(n=5):
    data = [random.randbytes(32) for _ in range(n)]
    for d in data:
        b = to_bits(d)
        v = sac_vals(b)
        # print([v * 100 for v in v])
        print(sum(v) / len(v) * 100)


def test_balance1(bits: list[int]):
    return bits.count(1) / len(bits)


def test_balance(n=5):
    # random.seed(1337)
    data = [random.randbytes(32) for _ in range(n)]
    c = 0
    for d in data:
        h = sha3_256_enc(d)
        bal = test_balance1(to_bits(h))
        print(bal, d, h)
        c += bal
    print(c / n)

import json

def test_distribution(n=4, m=10, hash_f=sha3_256_enc):
    counts = [0] * 2 ** n
    for _ in range(m):
        r = random.randbytes(32)
        h = hash_f(r)
        b = from_bits1(to_bits(h)[:n])
        print(b)
        counts[b] += 1
        print(counts)
    x = list(range(2**n))
    plt.xlabel("Value")
    plt.ylabel("Occurrences")
    plt.xticks(x)
    plt.stem(x, counts, markerfmt=' ')
    plt.ylim(top=100)
    with open('res.txt', 'w') as f:
        f.write(json.dumps(counts))
    plt.show()


def convert(x):
    if type(x) == str:
        return x.encode('ascii')
    elif type(x) == list:
        return bytes(x)
    return x


if __name__ == "__main__":
    # # test_distribution(hash_f=lambda d: sha3_256(d).digest())
    # print(sha3_256_enc("AAA".encode('ascii')).hex())
    # msg = random.randbytes(32)

    # msgs = [[1] * 16, "aaa", "qwertyuiop", "asdfghjkjl", "zxcvbnm", "kieadbwakidbnoipwdnwlkidnkslwdnwoidnwdnwkdnkdn",
    #         "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    #         "kawdbnawlkdnlaksndlskdknlsnd", "awidhnwasidnwoaidnwaoisd", "dwiuhdbuiwbduwdbwqigr387wui",
    #         "ausdisuabdiusadbiud", "doiwhdiowhdiowhdiwodhwiod", "oiwqhdoiwdhwiohdfwoq3rhg83rh"]
    # data = [convert(msg) for msg in msgs]
    # print([d for d in data])
    # res = [sha3_256_enc(d) for d in data]

    # print([r.hex() for r in res])
    # e = [sha3_256(d).digest() for d in data]
    # print(e)
    # print([ee.hex() for ee in e])

    # # find_collision(e, 17, hash_f=lambda d: sha3_256_enc(d))
    # # print()
    # get_nonlinearity_chart(check_nonlinearity(data), check_nonlinearity(res))

    # test_distribution(n=4, m=500)
    find_collision(10, 5)