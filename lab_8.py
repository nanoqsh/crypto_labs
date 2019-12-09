# DES

import sys


def print_bits(bits, intro=''):
    print(intro, end='')
    for bit in bits:
        print('1' if bit else '0', end='')
    print()

    return bits


def print_hex(bits, intro=''):
    print(intro, end='')
    for n in range(0, len(bits), 8):
        print(hex(bits_to_n(bits[n:n+8]))[2:], end=' ')
    print()

    return bits


def str_to_bits(s, n=64):
    if len(s) != n:
        raise Exception('Invalid len of string', s, 'in str_to_bits')

    for c in s:
        if c != '0' and c != '1':
            raise Exception('Invalid string', s, 'in str_to_bits')

    return tuple(map(lambda c: c == '1', s))


def bytearray_to_bits(arr):
    res = ()
    for byte in arr:
        res += n_to_bits(byte)

    return res


def n_to_bits(n, l=8):
    return tuple((n >> i) & 1 for i in reversed(range(l)))


def bits_to_n(bits):
    return sum([int(bit) * 2 ** i for i, bit in enumerate(reversed(bits))])


sn = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ],
]


def si(bits6, i):
    b1, b2, b3, b4, b5, b6 = bits6
    return n_to_bits(sn[i][bits_to_n((b1, b6))][bits_to_n((b2, b3, b4, b5))], 4)


def ip(bits64):
    t = [
        58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28,	20,	12,	4,
        62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7,
    ]

    return tuple(bits64[i - 1] for i in t)


def ip_inverted(bits64):
    t = [
        40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25,
    ]

    return tuple(bits64[i - 1] for i in t)


def e(bits32):
    t = [
        32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1,
    ]

    return tuple(bits32[i - 1] for i in t)


def p(bits32):
    t = [
        16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25,
    ]

    return tuple(bits32[i - 1] for i in t)


def xor(a, b):
    return tuple(map(lambda p: p[0] != p[1], zip(a, b)))


def s(bits48):
    n = 6
    res = ()
    for bits4 in tuple(si(bits48[i:i + n], r) for r, i in enumerate(range(0, 48, n))):
        res += bits4

    return res


def f(r_bits32, key_bits48):
    return p(s(xor(e(r_bits32), key_bits48)))


def ls(bits):
    b1, *bn = bits
    return (*bn, b1)


def expand_to_8bit(bits7):
    return (0, *bits7) if sum(bits7) % 2 == 0 else (1, *bits7)


def expand_to_64bit(bits56):
    n = 7
    res = ()
    for t in tuple(expand_to_8bit(bits56[i:i + n]) for i in range(0, 56, n)):
        res += t

    return res


def pc1(bits64):
    t = [
        57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4,
    ]

    return tuple(bits64[i - 1] for i in t)


def pc2(bits56):
    t = [
        14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32,
    ]

    return tuple(bits56[i - 1] for i in t)


def lshift(bits, i):
    if [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1][i] == 1:
        return ls(bits)
    else:
        return ls(ls(bits))


def split_bits(bits, n):
    return bits[:n], bits[n:]


def gen_keys(bits56):
    c, d = split_bits(pc1(expand_to_64bit(bits56)), 28)
    keys = []

    for i in range(16):
        c = lshift(c, i)
        d = lshift(d, i)
        keys.append(pc2((*c, *d)))

    return keys


def des(block_bits64, key_bits56, encrypt=True):
    l, r = split_bits(ip(block_bits64), 32)
    keys = gen_keys(key_bits56)
    
    for i in range(16):
        k = keys[i] if encrypt else keys[15 - i]
        l, r = r, xor(l, f(r, k))
    
    return ip_inverted((*l, *r))


def main(argv):
    encrypt = True
    block = ()
    key = ()

    for arg in argv:
        if arg.startswith('key='):
            key = str_to_bits(arg.split('=')[1], 56)

        if arg.startswith('str_key='):
            key = bytearray_to_bits(arg.split('=')[1].encode('utf-8'))

        if arg.startswith('block='):
            block = str_to_bits(arg.split('=')[1], 64)

        if arg.startswith('str_block='):
            block = bytearray_to_bits(arg.split('=')[1].encode('utf-8'))

        if arg == 'd':
            encrypt = False
    
    if key and block:
        print_hex(key, 'key: ')
        print_hex(block, 'block: ')
        print_hex(des(block, key, encrypt), 'encrypted: ' if encrypt else 'decrypted: ')


main(sys.argv)
