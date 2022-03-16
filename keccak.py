#!/bin/env python3
from utils import from_bits, to_bits, xorv
from functools import reduce
from itertools import product
from const import *


def pad_data(data: list[int], r: int) -> list[int]:
    pad = (r - len(data) % r) * '0'
    pad = [int(p) for p in pad]
    pad[0], pad[-1] = 1, 1
    return data + pad


rc = [[1] * 64] * 24
w = 3


def parity(v):
    return reduce(int.__xor__, v)


def block_perm(block: list[int], l: int) -> list[int]:
    def aget(i, j, k):
        return a[i % 5][j % 5][k % w]
    a = [[[block[(5*i+j)*w+k] for k in range(w)] for j in range(5)] for i in range(5)]
    N = 5 * 5 * w
    for r in range(12 + 2*l):
        a1 = [[[[0] for _ in range(w)] for _ in range(5)] for _ in range(5)]
        for i, (j, k) in product(range(5), product(range(5), range(w))):
            a1[i][j][k] = a[i][j][k] ^ parity([aget(m, j-1, k) for m in range(5)]) ^ parity([aget(m, j+1, k-1) for m in range(5)])

        a = a1
        print(a)
        exit(0)


def sha3_256_enc(data: bytes) -> bytes:
    r = 1088
    c = 512
    l = 6
    d = 256
    b = r + c
    state = [0] * b
    bits = to_bits(data)
    padded = pad_data(bits, r)
    n = len(padded)
    for i in range(0, n, r):
        block = padded[i:i+r]
        tmp = block + [0] * c
        tmp = xorv(tmp, state)
        state = block_perm(tmp, l)
    res = state[:d]
    return bytes(from_bits(res))


if __name__ == "__main__":
    msg = "abcd"
    data = msg.encode('ascii')
    print(data.hex())
    res = sha3_256_enc(data)
    print(res.hex())

# data:
# 1, 1, 0
# padding:
# 1, 1, 0, 1, 0, 0, ..., 1 x r=256
