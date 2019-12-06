# Vertical permutation cipher

import sys
import math


def fst(p):
    return p[0]


def snd(p):
    return p[1]


def key_input():
    raw = input('Input key: ').split()
    return tuple(map(int, raw))


def encrypt(message, key):
    table = ['' for i in range(len(key))]

    for i, m in enumerate(message):
        table[i % len(key)] += m

    return ''.join(map(snd, sorted(zip(key, table), key=fst)))


def decrypt(message, key):
    message_len = len(message)
    cols = len(key)
    rows = message_len // cols
    rem = message_len % cols
    table = ['' for i in range(cols)]
    positions = list(map(fst, sorted(enumerate(key), key=snd)))
    
    for i in range(cols):
        d = rows + int(i < rem)
        table[positions[i]] = message[:d]
        message = message[d:]

    result = ''
    for _ in range(math.ceil(message_len / cols)):
        for i in range(cols):
            if table[i]:
                result += table[i][0]
                table[i] = table[i][1:]

    return result


def main(argv):
    message = ''
    key = ()
    only_decrypt = False

    for arg in argv:
        if arg.startswith('message='):
            message = arg.split('=')[1]

        if arg.startswith('key='):
            raw = arg.split('=')[1].split(',')
            key = tuple(map(int, raw))

        if arg == 'd':
            only_decrypt = True

    if key == ():
        key = key_input()
    
    if only_decrypt:
        print('key:', key)
        print('decrypted:', decrypt(message, key))
    else:
        en = encrypt(message, key)
        print('key:', key)
        print('encrypted:', en)
        print('decrypted:', decrypt(en, key))


main(sys.argv)
