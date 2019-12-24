# RSA

import sys
import math


DEBUG = False


def get_n(p, q):
    return p * q


def phi_pq(p, q):
    return (p - 1) * (q - 1)


def test_gcd(x, y):
    return math.gcd(x, y) == 1


def select_e(p, q, d):
    phi_n = phi_pq(p, q)

    if DEBUG:
        print('phi n:', phi_n)

    for x in range(2, phi_n):
        if test_gcd(phi_n, x) and (d * x) % phi_n == 1:
            
            if DEBUG:
                print('e:', x)
            
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


ENCRYPT_MODE = 0
DECRYPT_MODE = 1
BOTH_MODE = 2


def main(argv):
    global DEBUG

    p = None
    q = None
    d = None
    source_filename = None
    encrypted_filename = None
    decrypted_filename = None
    mode = BOTH_MODE

    for arg in argv:
        if arg.startswith('p='):
            p = int(arg.split('=')[1])

        if arg.startswith('q='):
            q = int(arg.split('=')[1])

        if arg.startswith('d='):
            d = int(arg.split('=')[1])
        
        if arg.startswith('source=') or arg.startswith('source_file='):
            source_filename = arg.split('=')[1]

        if arg.startswith('encrypted_file=') or arg.startswith('ef='):
            encrypted_filename = arg.split('=')[1]
        
        if arg.startswith('decrypted_file=') or arg.startswith('df='):
            decrypted_filename = arg.split('=')[1]

        if arg == 'd':
            mode = DECRYPT_MODE

        if arg == 'e':
            mode = ENCRYPT_MODE

        if arg == 'de' or arg == 'ed':
            mode = BOTH_MODE

        if arg == 'debug':
            DEBUG = True
    
    if p is None:
        p = int(input('Enter P: '))
    
    if q is None:
        q = int(input('Enter Q: '))

    if d is None:
        d = int(input('Enter D: '))
    
    if source_filename is None and mode != DECRYPT_MODE:
        source_filename = int(input('Enter source filename: '))
    
    if encrypted_filename is None:
        encrypted_filename = int(input('Enter encrypted filename: '))

    if decrypted_filename is None and mode != ENCRYPT_MODE:
        decrypted_filename = int(input('Enter decrypted filename: '))

    n = get_n(p, q)

    if DEBUG:
        print('p:', p)
        print('q:', q)
        print('d:', d)
        print('n:', n)

    if mode == ENCRYPT_MODE or mode == BOTH_MODE:
        e = select_e(p, q, d)
        pub_key = e, n
        data = encrypt_file(source_filename, pub_key)
        save_file(data, encrypted_filename)

    if mode == DECRYPT_MODE or mode == BOTH_MODE:
        priv_key = d, n
        decrypted_data = decrypt_file(encrypted_filename, priv_key)
        save_file(decrypted_data, decrypted_filename)


main(sys.argv)
