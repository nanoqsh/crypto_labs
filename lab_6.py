# Vertical permutation cipher

import sys
import math


def str_to_key(s):
    return tuple(map(int, s.split()))


def fst(p):
    return p[0]


def snd(p):
    return p[1]


def encrypt(message, key):
    table = ['' for i in range(len(key))]

    for i, m in enumerate(message):
        table[i % len(key)] += m

    return ''.join(map(snd, sorted(zip(key, table), key=fst)))


def positions_from_key(key):
    return list(map(fst, sorted(enumerate(key), key=snd)))


def split_at(s, n):
    return s[:n], s[n:]


def decrypt(message, key):
    message_len = len(message)
    cols = len(key)
    rows = message_len // cols
    table = ['' for i in range(cols)]
    positions = positions_from_key(key)
    
    for i in range(cols):
        d = rows + int(i < message_len % cols)
        table[positions[i]], message = split_at(message, d)

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
            raw = arg.split('=')[1]
            key = str_to_key(raw.replace(',',' '))

        if arg == 'd':
            only_decrypt = True

    if not key:
        key = str_to_key(input('Input key: '))

    if not message:
        message = input('Input message: ')

    print('key:', key)
    print('message:', message)
    
    if only_decrypt:
        print('decrypted:', decrypt(message, key))
    else:
        en = encrypt(message, key)
        print('encrypted:', en)
        print('decrypted:', decrypt(en, key))


main(sys.argv)
