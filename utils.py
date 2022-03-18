from itertools import chain
def to_bits(d, g=8):
    return list(chain.from_iterable((c >> i & 1 for i in range(g)) for c in d))

from functools import reduce
def from_bits(b, g=8):
    return [reduce(lambda x,y: x<<1|y, g[::-1]) for g in zip(*(iter(b),)*g)]

def xorv(a: list[int], b: list[int]):
    return [b1 ^ b2 for (b1, b2) in zip(a, b)]

def andv(a: list[int], b: list[int]):
    return [b1 & b2 for (b1, b2) in zip(a, b)]