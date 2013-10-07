import logging
import os
import unittest

import numpy as np
from scipy.misc import imresize
from stl_tools import text2array, numpy2stl


"""
Some basic tests for stl_tools
"""

logging.basicConfig(level=logging.DEBUG)


class TestSTL(unittest.TestCase):

    def test_text(self):
        """ Tests creation of an image array from a text expression.
        Covers the text2png and text2array functions.
        """

        A = text2array("TEST", fontsize=1000)
        A = imresize(A, (100, 100))
        #np.savetxt("TEST.csv", A, delimiter=',')
        B = np.loadtxt("TEST.csv", delimiter=',')
        r = np.linalg.norm(A - B) / np.linalg.norm(B)
        self.assertAlmostEqual(r, 0.0)

    def test_png(self):
        """ Tests creation of an STL from a PNG.
        Covers the text2array function.
        """

        # test ascii output
        A = imresize([[0, 1], [1, 0]], (64, 64))
        numpy2stl(A, "OUT_.stl", scale=0.05, mask_val=3., ascii=True)
        reference = open("TEST_ascii.stl", 'rb')
        new = open("OUT_.stl", 'rb')
        newlines = new.readlines()
        reflines = reference.readlines()
        new.close(), reference.close()
        self.assertEqual(newlines, reflines)

        # test binary output
        numpy2stl(A, "OUT_.stl", scale=0.05, mask_val=6.)
        reference = open("TEST_bin.stl", 'rb')
        new = open("OUT_.stl", 'rb')
        newlines = new.readlines()
        reflines = reference.readlines()
        new.close(), reference.close()
        self.assertEqual(newlines, reflines)
        os.remove("OUT_.stl")

if __name__ == '__main__':
    unittest.main()
