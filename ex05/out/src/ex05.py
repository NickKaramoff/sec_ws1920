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
    import ex05_testdata_lecturer as testdata  # @UnresolvedImport @UnusedImport

except:
    import ex05_testdata as testdata  # @UnusedImport


import os
import subprocess
import sys
import unittest


unittest.TestLoader.sortTestMethodsUsing = None
PYTHON = "python3"
PYERROR = "For running your solutions we call '{}'.\nThe name might be different for your installation (e.g. on Windows)\n"


class Ex05(unittest.TestCase):

    TASKS = 0
    MY_DIR = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def call(tool, params):
        script = os.path.join(Ex05.MY_DIR, tool)
        cmd = '{} "{}" {}'.format(PYTHON, script, params)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()

        # if p.returncode != 0:
        #    sys.stderr.write(PYERROR.format(PYTHON))

        return out, err, p.returncode

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

        return line

    def test_03_sendpacket(self):
        _, out, _ = Ex05.call("send_packet.py", "")
        self.assertTrue(testdata.verify_synopsis("send_packet", out))
        Ex05.TASKS += 1

    def test_04_portknocker(self):
        _, out, _ = Ex05.call(os.path.join("port_knocker", "client.py"), "")
        self.assertTrue(testdata.verify_synopsis("client", out))
        Ex05.TASKS += 1

        _, out, _ = Ex05.call(os.path.join("port_knocker", "server.py"), "")
        self.assertTrue(testdata.verify_synopsis("server", out))
        Ex05.TASKS += 1

    def test_XX(self):
        if Ex05.TASKS > 0:
            print(
                "[*] The synopsis are okay for {} out of {} tasks! 👍".format(Ex05.TASKS, 3))
        else:
            print("[*] Unfortunately, non of the synopsis are as expected (yet 😉)")


if __name__ == "__main__":
    unittest.main()
