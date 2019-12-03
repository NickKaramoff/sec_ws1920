import argparse

def extended_gcd(a, b):
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a
    ob = b
    while b != 0:
        q = a // b
        (a, b)  = (b, a % b)
        (x, lx) = ((lx - (q * x)),x)
        (y, ly) = ((ly - (q * y)),y)
    if (lx < 0): lx += ob
    if (ly < 0): ly += oa
    return lx

def euler(n):
    res = 1
    i = 2
    while (i * i <= n):
        p = 1
        while (n % i == 0):
            n /= i
            p *= i
        p /= i
        if (p != 0):
            res *= (p * (i - 1))
        i += 1
    n = n - 1
    if (n == 0):
        return res
    else:
        return n * res


parser = argparse.ArgumentParser()
parser.add_argument("-e", "--exponent", type=int, nargs="?", const=211,default=211, help="specifying the exponent")
parser.add_argument("-n", "--modulus", type=int, nargs="?", const=67063,default=67063, help="specifying the modulus")
parser.add_argument("-c","--ciphertext", type=int, default=19307,nargs="?", const=19307, help="specifying the "
                                                                                              "ciphertext to break")

args = parser.parse_args()

d = extended_gcd(args.exponent, euler(args.modulus))
m = (args.ciphertext**d)%args.modulus
print(m)

