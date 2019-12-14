#!/usr/bin/env python3

'''
@author: Christian Wressnegger
'''

import argparse
import os
import re
import sys

from urllib.parse import unquote
from gnupg import GPG


def __read_line(self, fname):
    my_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        line = None
        with open(os.path.join(my_dir, fname), 'r') as f:
            for line in f:
                break

        self.assertTrue(line, "No data provided")
    except IOError:
        self.assertTrue(False, "Unable to read file")

    return line


def error(s):
    sys.stderr.write("[!] {}\n".format(s))


def main(name, fingerprint, check_online=False):
    fprint = re.sub(r'\s+', '', fingerprint.strip()).upper()
    if len(fprint) != 40:
        error("The length of the fingerprint seems to be off :(")
        return 1

    if check_online:
        gpg = GPG()
        result = gpg.search_keys(fprint, 'keys.openpgp.org')

        if not result:
            error("Cannot find a key with fingerprint '{}'. Did you upload your key to keys.openpgp.org?".format(fingerprint))
            return 2

        if name not in map(extract_name_from_uid, result.uids):
            error("Cannot find name '{}' in keys uids: '{}'".format(name, "', '".join(map(unquote, result.uids))))
            return 3

    fprint = ' '.join(str(fprint[i:i + 4]) for i in range(0, len(fprint), 4))
    print("{}\t{}".format(name, fprint))
    return 0


def extract_name_from_uid(uid):
    return ' '.join(unquote(uid).split(' ')[:-1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", metavar="STR", action="store", type=str, default=None, required=True,
                        help="Your GPG fingerprint.")
    parser.add_argument("--fingerprint", metavar="STR", action="store", type=str, default=None,  required=True,
                        help="Your GPG fingerprint.")
    parser.add_argument("--skip-online-check", dest="check_online", action="store_false", default=True,
                        help="Omit check at the key server.")

    args = parser.parse_args()

    try:
        sys.exit(main(args.name, args.fingerprint, args.check_online))
    except Exception as e:
        sys.stderr.write("{}\n".format(e))
        sys.exit(666)
