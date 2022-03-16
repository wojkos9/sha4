from utils import to_bits, xorv


def pad_data(data: list[int], r: int) -> list[int]:
    pad = (r - len(data) % r) * '0'
    pad = [int(p) for p in pad.split()]
    pad[0], pad[-1] = 1, 1
    return data + pad


def block_perm(block: list[int]) -> list[int]:
    pass

def sha3_256_enc(data: bytes) -> list[int]:
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
        state = block_perm(tmp)
    res = state[:d]
    return res


if __name__ == "__main__":
    msg = "abcd"
    data = msg.encode('ascii')
    print(data)
    sha3_256_enc(data)

# data:
# 1, 1, 0
# padding:
# 1, 1, 0, 1, 0, 0, ..., 1 x r=256
