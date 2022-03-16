from utils import to_bits


def pad_data(data: list[int], r: int) -> list[int]:
    pad = (r - len(data) % r) * '0'
    pad = [int(p) for p in pad.split()]
    pad[0], pad[-1] = 1, 1
    return data + pad


def sha3_256_enc(data: bytes):
    r = 256
    l = 6
    bits = to_bits(data)
    padded = pad_data(bits, r)
    print(padded)


if __name__ == "__main__":
    msg = "abcd"
    data = msg.encode('ascii')
    print(data)
    sha3_256_enc(data)

# data:
# 1, 1, 0
# padding:
# 1, 1, 0, 1, 0, 0, ..., 1 x r=256
