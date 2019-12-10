# RSA

import sys
import math


def phi_pq(p, q):
    return (p - 1) * (q - 1)


def test_gcd(x, y):
    return math.gcd(x, y) == 1


def select_e(p, q, d):
    phi_n = phi_pq(p, q)
    print('phi n:', phi_n)

    for x in range(2, phi_n):
        if test_gcd(phi_n, x):
            return x
    
    raise Exception('e not found!')


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
    e = select_e(61, 71, 9577)
    print('e:', e)


main(sys.argv)
