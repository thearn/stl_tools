import logging
import os
import unittest
import os
import numpy as np
from scipy.misc import imresize
from stl_tools import text2array, numpy2stl
from qimshow import qimshow

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
        assert A[np.where(A != 0)].size / float(A.size) > 0.2

    def test_png(self):
        """ Tests creation of an STL from a PNG.
        Covers the text2array function.
        """

        # test ascii output
        A = imresize([[0, 1], [1, 0]], (64, 64))
        numpy2stl(A, "OUT_.stl", scale=0.05, mask_val=3., ascii=True)
        os.path.exists("OUT_.stl")

        # test binary output
        A = imresize([[0, 1], [1, 0]], (64, 64))
        numpy2stl(A, "OUT_.stl", scale=0.05, mask_val=3., ascii=False)
        os.path.exists("OUT_.stl")

        os.remove("OUT_.stl")

if __name__ == '__main__':
    unittest.main()
