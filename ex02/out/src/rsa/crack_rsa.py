import argparse


def modular_inverse(num, m):
    """
    Calculates the modular inverse of a number with a given modulus

    :param num: number to find modular inverse for
    :param m: number to regard as mod
    :return: modular inverse for num (mod m)
    """

    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = num
    ob = m

    while m != 0:
        q = num // m
        (num, m) = (m, num % m)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)

    if lx < 0:
        lx += ob
    if ly < 0:
        ly += oa
    return lx


def euler_phi(modulus):
    """
    Calculates the value of the Euler totient function for a given number

    :param modulus: number to find the Euler function value
    :return: phi(given number)
    """
    result = modulus
    p = 2

    while p * p <= modulus:
        if modulus % p == 0:
            while modulus % p == 0:
                modulus //= p
            result *= (1 - (1 / p))
        p += 1

    if modulus > 1:
        result *= (1 - (1 / modulus))

    return int(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--exponent",
                        type=int,
                        help="specifying the exponent")
    parser.add_argument("-n", "--modulus",
                        type=int,
                        help="specifying the modulus")
    parser.add_argument("-c", "--ciphertext",
                        type=int,
                        help="specifying the ciphertext to break")

    args = parser.parse_args()

    phi_n = euler_phi(args.modulus)
    decr_key = modular_inverse(args.exponent, phi_n)
    message = (args.ciphertext ** decr_key) % args.modulus
    print(message)
