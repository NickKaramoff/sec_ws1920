import argparse


def extended_euclidian(a: int, b: int) -> (int, int, int):
    """
    Calculates the gcd of two numbers as well as quotients ``x`` and ``y`` such,
    that ``ax + by = gcd(a,b)``

    :param a: number
    :param b: number
    :return: tuple of gcd(a,b), x and y
    """

    x = 0
    y = 1

    if a == 0:
        return b, x, y

    g, x_1, y_1 = extended_euclidian(b % a, a)
    x = y_1 - (b // a) * x_1
    y = x_1

    return g, x, y


def euler_phi(modulus: int) -> int:
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
    decr_key = phi_n + extended_euclidian(args.exponent, phi_n)[1]
    message = (args.ciphertext ** decr_key) % args.modulus
    print(message)
