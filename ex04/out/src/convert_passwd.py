import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts passwords from task '
                                                 'to a UNIX-like passwd file')
    parser.add_argument('input', help='Original input file')
    parser.add_argument('output', help='Transformed passwords')
    args = parser.parse_args()

    with open(args.input, 'r') as fr:
        with open(args.output, 'w') as fw:
            for line in fr.readlines():
                fw.write(line.strip() + ':1:1:user:/bin/sh:/root\n')