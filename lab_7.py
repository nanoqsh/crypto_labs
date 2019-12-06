# S-DES

import sys


def print_bits(bits, intro=''):
    print(intro, end='')
    for bit in bits:
        print('1' if bit else '0', end='')
    print()

    return bits


def str_to_bits(s, n=8):
    if len(s) != n:
        raise Exception('Invalid len of string', s, 'in str_to_bits')

    for c in s:
        if c != '0' and c != '1':
            raise Exception('Invalid string', s, 'in str_to_bits')

    return tuple(map(lambda c: c == '1', s))


def p10(bits):
    b1, b2, b3, b4, b5, b6, b7, b8, b9, b10 = bits
    return b3, b5, b2, b7, b4, b10, b1, b9, b8, b6


def p8(bits):
    _, _, b3, b4, b5, b6, b7, b8, b9, b10 = bits
    return b6, b3, b7, b4, b8, b5, b10, b9


def p4(bits):
    b1, b2, b3, b4 = bits
    return b2, b4, b3, b1


def ls1(bits):
    b1, b2, b3, b4, b5, b6, b7, b8, b9, b10 = bits
    return b2, b3, b4, b5, b1, b7, b8, b9, b10, b6


def ls2(bits):
    return ls1(ls1(bits))


def key_pair(bits):
    key = ls1(p10(bits))
    return p8(key), p8(ls2(key))


def ip(bits):
    b1, b2, b3, b4, b5, b6, b7, b8 = bits
    return b2, b6, b3, b1, b4, b8, b5, b7


def ip_inverted(bits):
    b1, b2, b3, b4, b5, b6, b7, b8 = bits
    return b4, b1, b3, b5, b7, b2, b8, b6


def ep(bits):
    b1, b2, b3, b4 = bits
    return b4, b1, b2, b3, b2, b3, b4, b1


def n_to_2bits(n):
    if n == 0:
        return (0, 0)
    elif n == 1:
        return (0, 1)
    elif n == 2:
        return (1, 0)
    elif n == 3:
        return (1, 1)
    else:
        raise Exception('Invalid number n', n)


def bits_to_n(bits):
    b1, b2 = bits

    if not b1 and not b2:
        return 0
    elif not b1 and b2:
        return 1
    elif b1 and not b2:
        return 2
    elif b1 and b2:
        return 3


def s(a, b, table):
    return n_to_2bits(table[bits_to_n(a)][bits_to_n(b)])


def s0(bits):
    b1, b2, b3, b4 = bits

    table = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 1],
    ]

    return s((b1, b4), (b2, b3), table)


def s1(bits):
    b1, b2, b3, b4 = bits

    table = [
        [1, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3],
    ]

    return s((b1, b4), (b2, b3), table)


def f(bits, key):
    b1, b2, b3, b4, b5, b6, b7, b8 = xor(ep(bits), key)
    q1, q2 = s0((b1, b2, b3, b4))
    q3, q4 = s1((b5, b6, b7, b8))
    return p4((q1, q2, q3, q4))


def fk(bits, key):
    b1, b2, b3, b4, b5, b6, b7, b8 = bits
    q1, q2, q3, q4 = xor((b1, b2, b3, b4), f((b5, b6, b7, b8), key))
    return q1, q2, q3, q4, b5, b6, b7, b8


def xor(a, b):
    return tuple(map(lambda p: p[0] != p[1], zip(a, b)))


def sw(bits):
    b1, b2, b3, b4, b5, b6, b7, b8 = bits
    return b5, b6, b7, b8, b1, b2, b3, b4


def crypt(bit8_block, k1, k2):
    return print_bits(ip_inverted(
        print_bits(fk(
            print_bits(sw(
                print_bits(fk(
                    print_bits(ip(
                        bit8_block
                        ), '       ip: '), k1
                        ), '       fk: ')
                        ), '       sw: '), k2
                        ), '       fk: ')
                        ), '     ip-1: ')


def main(argv):
    message = ()
    key = ()
    encryption = True

    for arg in argv:
        if arg.startswith('key='):
            key = str_to_bits(arg.split('=')[1], 10)

        if arg.startswith('message='):
            message = str_to_bits(arg.split('=')[1])

        if arg == 'd':
            encryption = False
    
    if not key:
        key = str_to_bits(input('Enter a key: '), 10)

    if not message:
        message = str_to_bits(input('Enter a message'))
    
    print_bits(key, '      key: ')
    print_bits(message, '  message: ')

    k1, k2 = key_pair(key)
    print_bits(k1, '       k1: ')
    print_bits(k2, '       k2: ')

    if encryption:
        print_bits(crypt(message, k1, k2), 'encrypted: ')
    else:
        print_bits(crypt(message, k2, k1), 'decrypted: ')


main(sys.argv)
