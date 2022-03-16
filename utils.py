from itertools import chain
def to_bits(d, g=8):
    return list(chain.from_iterable((c >> i & 1 for i in range(g)) for c in d))