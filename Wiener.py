# Resource: https://profs.info.uaic.ro/~siftene/Wiener.pdf
# https://www.youtube.com/watch?v=OpPrrndyYNU
# If q < p < 2*q and d <= 1/3 * sqr(4, N) the attack will succeed

import cmath


def euclid(a, b):
    return a // b, a % b


def continuous_conv(n, d):
    next = []
    a = n
    b = d
    while b != 0:
        (q, r) = euclid(a, b)
        next.append(q)
        a = b
        b = r
    return next


def continuous_fraction(a):
    l = len(a)
    fraction = []
    h0 = 1
    h1 = 0
    k0 = 0
    k1 = 1
    count = 0
    while count < l:
        h = a[count] * h1 + h0
        h0 = h1
        h1 = h
        k = a[count] * k1 + k0
        k0 = k1
        k1 = k
        fraction.append((k, h))
        count += 1
    return fraction


def wiener(e, n):
    fc = continuous_fraction(continuous_conv(e, n))
    for count in range(0, len(fc)):
        k, d = fc[count]
        if k == 0 or d == 1:
            continue
        if d % 2 == 0:
            continue
        if (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) / k
        a = 1
        b = -(n - phi + 1)
        c = n
        delta = (b ** 2) - (4 * a * c)
        sol1 = (-b - cmath.sqrt(delta)) / (2 * a)  # solve quadratic equation
        sol2 = (-b + cmath.sqrt(delta)) / (2 * a)
        if sol1 * sol2 != n:
            continue
        print('p = ', sol1, ' q = ', sol2)
        return d
    return -1


def main():
    print('------ Wiener ------')
    e = 42667
    n = 64741
    d = wiener(e, n)
    if d != -1:
        print("Cracked the code and found the private exponent d = ", d, " and n = ", n)
    else:
        print('Code cannot be cracked')


main()
