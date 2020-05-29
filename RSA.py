# RSA algorithm is a public key encryption technique and is considered as the most secure way of encryption.
# Resource: https://www.di-mgt.com.au/rsa_alg.html#note5


import sympy
import time


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def convert_to_int(text):
    converted = []
    for letter in text:
        converted.append(ord(letter) - 96)
    return converted


def convert_to_ascii(text):
    converted = ''
    for number in text:
        converted = converted + chr(number + 96)
    return converted


def choose_e(phi, n):
    print('Choosing e...')
    for e in range(2 ** 31, 2, -1):
        if gcd(e, phi) == 1 and gcd(e, n) == 1:
            return e


def modular_inverse(a, m):  # modular inverse of e modulo phi
    m0 = m
    y = 0
    x = 1

    if m == 1:
        return 0

    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x = x + m0

    return x


def encrypt(text, public_key):
    key, n = public_key
    ctext = [pow(ord(char), key, n) for char in text]
    return ctext


def decrypt(ctext, private_key):
    key, n = private_key
    text = [chr(pow(char, key, n)) for char in ctext]
    return "".join(text)


def RSA():
    enc = []
    dec = []
    p = sympy.nextprime(2 ** 512)
    q = sympy.nextprime(p)
    print('p = ', p, ' q = ', q)
    n = p * q
    print('n = ', n)
    phi = (p - 1) * (q - 1)
    time_start1 = time.time()
    print('phi = ', phi)
    e = choose_e(phi, n)
    print('e = ', e)
    d = modular_inverse(e, phi)
    print('d = ', d)
    text = 'pythonisthebest'
    print('Plaintext: ', text)
    converted = convert_to_int(text)
    for number in converted:
        enc.append(pow(number, e, n))
    print('Encrypted text: ', enc)
    for number in enc:
        dec.append(pow(number, d, n))
    decrypted = convert_to_ascii(dec)
    print('Decrypted text: ', decrypted)
    time_finish1 = time.time()
    print('Time for classic decryption: ', time_finish1 - time_start1)
    return p, q, e, d, enc


# The CRT method of decryption is about four times faster overall
# Even though there are more steps in this procedure,
# the modular exponentiation to be carried out uses much shorter exponents and so it is less expensive in the end
def TCR(p, q, dP, dQ, c):
    qInv = modular_inverse(q, p)
    m1 = pow(c, dP, p)
    m2 = pow(c, dQ, q)
    h = (qInv * (m1 - m2)) % p
    m = m2 + h * q
    return m


def main():
    print('------ RSA ------')
    p, q, _, d, enc = RSA()
    time_start2 = time.time()
    dp = d % (p - 1)
    dq = d % (q - 1)
    text = ''
    for number in enc:
        text = text + chr(TCR(p, q, dp, dq, number) + 96)
    print('Decrypted using TCR: ', text)
    time_finish2 = time.time()
    print('Time for TCR decryption: ', time_finish2 - time_start2)


main()
