import argparse


def goofy_force(a, g, n):
    i = 0
    while (g ** i) % n != a:
        i += 1
    return i


parser = argparse.ArgumentParser()
parser.add_argument("-g", "--generator", type=int, nargs="?", const=10, default=10, help="")
parser.add_argument("-n", "--modulus", type=int, nargs="?", const=1783, default=1783, help="")
parser.add_argument("-a", "--alice", type=int, default=929, const=929, nargs="?", help="")
parser.add_argument("-b", "--bob", type=int, nargs="?", const=626, default=626, help="")

args = parser.parse_args()

print(args.generator ** (goofy_force(args.alice, args.generator, args.modulus) * goofy_force(args.bob, args.generator,args.modulus))%args.modulus)
