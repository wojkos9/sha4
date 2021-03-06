#!/bin/env python3
from itertools import product
from const import *
from utils import *


def pad_data(data: list[int], r: int) -> list[int]:
    pad = (r - len(data) % r) * '0'
    pad = [int(p) for p in pad]
    pad[0], pad[-1] = 1, 1
    return data + pad


rc = [[1] * 64] * 24
w = 64

rot = [[0,  36,   3,  41,  18],
    [1,  44,  10,  45,   2],
    [62,  6,  43,  15,  61],
    [28, 55,  25,  21,  56],
    [27, 20,  39,   8,  14]]


def parity(v: list[int]):
    return v[0] ^ v[1] ^ v[2] ^ v[3] ^ v[4]


def aget(a, i, j, k):
    return a[i % 5][j % 5][k % w]


def theta(a):
    return [[[a[i][j][k] ^ parity([a[m][(j-1)%5][k] for m in range(5)]) ^ parity([a[m][(j+1)%5][(k-1)%w] for m in range(5)]) for k in range(w)] for j in range(5)] for i in range(5)]


def rotv(vec, a):
    return vec[-a:] + vec[:-a]


def notv(vec):
    return [~e for e in vec]


def rho_pi(a):
    a1 = [[[0 for _ in range(w)] for _ in range(5)] for _ in range(5)]
    for x in range(5):
        for y in range(5):
            a1[y][(2 * x + 3 * y) % 5] = rotv(a[x][y], rot[x][y])
    return a1


def block_perm(block: list[int], l: int) -> list[int]:

    a = [[[block[(5*i+j)*w+k] for k in range(w)] for j in range(5)] for i in range(5)]
    for r in range(12 + 2*l):
        a = theta(a)
        a = rho_pi(a)
        a = chi_step(a)
        c = round_const[r]
        a = iota_step(a, c)
    return [a[i][j][k] for i, (j, k) in product(range(5), product(range(5), range(w)))]


def chi_step(a):
    a1 = [[[0 for _ in range(w)] for _ in range(5)] for _ in range(5)]
    for x in range(5):
        for y in range(5):
            a1[x][y] = xorv(a[x][y], andv((notv(a[(x + 1) % 5][y])), a[(x + 2) % 5][y]))
    return a1


def iota_step(a, r_const):
    a[0][0] = xorv(a[0][0], r_const)
    return a


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
