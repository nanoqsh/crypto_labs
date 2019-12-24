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
        if test_gcd(phi_n, x) and (d * x) % phi_n == 1:
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


def read_file(filename):
    with open(filename, 'rb') as f:
        return bytearray(f.read())


def save_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)


def encrypt(byte, pub_key):
    e, n = pub_key
    return pow_mod(byte, e, n)


def decrypt(bit32, priv_key):
    d, n = priv_key
    return pow_mod(bit32, d, n)


def encrypt_file(filename, pub_key):
    data = read_file(filename)
    encrypted = bytearray()
    for byte in data:
        s = encrypt(byte, pub_key)
        for encrypted_byte in s.to_bytes(2, byteorder='little'):
            encrypted.append(encrypted_byte)
    
    return encrypted


def decrypt_file(filename, priv_key):
    data = read_file(filename)
    decrypted = bytearray()

    for i in range(0, len(data), 2):
        bit32 = int.from_bytes(data[i:i+2], byteorder='little')
        decrypted.append(decrypt(bit32, priv_key))
    
    return decrypted


def main(argv):
    p = 61
    q = 71
    d = 9577
    filename = 'test.txt'
    e = select_e(p, q, d)
    print('e', e)
    n = p * q
    pub_key = e, n
    data = encrypt_file(filename, pub_key)
    print(data)
    print('len:', len(data))
    crypted_filename = 'test.crypted'
    save_file(data, crypted_filename)
    priv_key = d, n
    decrypted_data = decrypt_file(crypted_filename, priv_key)
    print(decrypted_data)
    print('len:', len(decrypted_data))


main(sys.argv)
