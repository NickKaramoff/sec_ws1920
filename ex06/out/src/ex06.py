#!/usr/bin/env python3

'''
@author: Christian Wressnegger
'''

import os
import unittest

unittest.TestLoader.sortTestMethodsUsing = None
PYTHON = "python3"
PYERROR = "For running your solutions we call '{}'.\nThe name might be different for your installation (e.g. on Windows)\n"


class Ex06(unittest.TestCase):

    TASKS = 0

    def xss_read_url(self, var):
        my_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            url = None
            with open(os.path.join(my_dir, "xss-var{}.url".format(var)), 'r') as f:
                for line in f:
                    url = line
                    break
            self.assertTrue(
                url and url.startswith("https://weird.sec.tu-bs.de"), "No URL!?")
        except IOError:
            self.assertTrue(False, "Unable to read file")

    def test_01_xss_var0(self):
        self.xss_read_url(0)
        Ex06.TASKS += 1

    def test_01_xss_var1(self):
        self.xss_read_url(1)
        Ex06.TASKS += 1

    def test_01_xss_var2(self):
        self.xss_read_url(2)
        Ex06.TASKS += 1

    def test_01_xss_var3(self):
        self.xss_read_url(3)
        Ex06.TASKS += 1

    def test_01_xss_var4(self):
        self.xss_read_url(4)
        Ex06.TASKS += 1

    def test_01_xss_var5(self):
        self.xss_read_url(5)
        Ex06.TASKS += 1

    def test_XX(self):
        if Ex06.TASKS > 0:
            print(
                "[*] Your submission contains solutions for {} out of {} tasks! 👍".format(Ex06.TASKS, 6))
        else:
            print("[*] Unfortunately, there are not valid solutions (yet 😉)")


if __name__ == "__main__":
    unittest.main()
