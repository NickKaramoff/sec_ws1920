#!/usr/bin/env python3

'''
@author: Christian Wressnegger
'''

try:
    # For evaluating the exercises we'll provide a similar but
    # different configuration that contains alternative input
    # values than those provided in the script that was handed
    # out (nothing mean though). Develop your solution robust
    # enough to work with various kinds and variations of input.
    import ex03_testdata_lecturer as testdata  # @UnresolvedImport @UnusedImport

except:
    import ex03_testdata as testdata  # @UnusedImport


import os
import re
import subprocess
import sys
import unittest

from urllib.parse import unquote
from gnupg import GPG

unittest.TestLoader.sortTestMethodsUsing = None
PYTHON = "python3"
PYERROR = "For running your solutions we call '{}'.\nThe name might be different for your installation (e.g. on Windows)\n"


class Ex03(unittest.TestCase):

    CHECK_GPGKEY_ONLINE = True

    TASKS = 0
    MY_DIR = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def extract_name_from_uid(uid):
        return ' '.join(unquote(uid).split(' ')[:-1])

    @staticmethod
    def call(tool, params):
        script = os.path.join(Ex03.MY_DIR, tool)
        cmd = '{} "{}" {}'.format(PYTHON, script, params)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, _ = p.communicate()

        if p.returncode != 0:
            sys.stderr.write(PYERROR.format(PYTHON))

        return out, p.returncode

    def read_line(self, fname):
        my_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            line = None
            with open(os.path.join(my_dir, fname), 'r') as f:
                for line in f:
                    break

            self.assertTrue(line, "No data provided")
        except IOError:
            self.assertTrue(False, "Unable to read file")

        return line.strip()

    def test_03_mitm(self):
        out, _ = Ex03.call("mitm.py", 'weird.sec.tu-bs.de 3333')
        self.assertTrue(testdata.verify_msgs(out))

        s = self.read_line("flag.txt")
        self.assertTrue(testdata.verify_flag(s))
        Ex03.TASKS += 1

    def test_04_gpg(self):
        fprint_raw = self.read_line("fingerprint.txt").split('\t')[-1]
        fprint = re.sub(r'\s+', '', fprint_raw.strip()).upper()
        self.assertEqual(len(fprint), 40)

        if Ex03.CHECK_GPGKEY_ONLINE:
            gpg = GPG()
            result = gpg.search_keys(fprint, 'keys.openpgp.org')

            if not result:
                self.fail(
                    "Cannot find a key with fingerprint '{}'".format(fprint_raw))
            name = ' '.join(self.read_line(os.path.join("..", "NAME")).split(' ')[:-1])
            if name not in map(Ex03.extract_name_from_uid, result.uids):
                self.fail("Cannot find name '{}' in keys uids: '{}'".format(name,"', '".join(map(unquote, result.uids))))

        Ex03.TASKS += 1

    def test_XX(self):
        if Ex03.TASKS > 0:
            print("[*] {} out of {} exercises work flawlessly! 👍".format(Ex03.TASKS, 2))
        else:
            print("[*] Unfortunately, non of the exercises work as expected (yet 😉)")


if __name__ == "__main__":
    unittest.main()
