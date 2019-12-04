import argparse


def goofy_force(key, g, n):
    i = 0
    while (g ** i) % n != key:
        i += 1
    return i


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--generator",
                        type=int,
                        help="Generator")
    parser.add_argument("-n", "--modulus",
                        type=int,
                        help="Modulus")
    parser.add_argument("--alice",
                        type=int,
                        help="Alice's key")
    parser.add_argument("--bob",
                        type=int,
                        help="Bob's key")

    args = parser.parse_args()

    print(args.generator ** (goofy_force(args.alice, args.generator, args.modulus) * goofy_force(args.bob, args.generator,args.modulus)) % args.modulus)
