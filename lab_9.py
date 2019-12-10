# RSA

import sys


def pow_mod(a, b, n):
    if b == 0:
        return 1

    d = 1
    for bit in bin(b)[2:]:
        d = (d * d) % n
        if bit == '1':
            d = (d * a) % n
    
    return d


def main(argv):
    pass


main(sys.argv)
