import logging
import os
import unittest
import os
import numpy as np
from scipy.misc import imresize
from stl_tools import text2array, numpy2stl, text2png
from qimshow import qimshow

"""
Some basic tests for stl_tools
"""

logging.basicConfig(level=logging.DEBUG)


class TestSTL(unittest.TestCase):

    def test_text2png(self):
        """ Tests creation of an image array from a text expression.
        Covers the text2png and text2array functions.
        """

        text2png("TEST", fontsize=1000)
        assert os.path.exists("TEST.png")
        os.remove("TEST.png")

    def test_text2array(self):
        """ Tests creation of an image array from a text expression.
        Covers the text2png and text2array functions.
        """

        A = text2array("TEST", fontsize=1000)
        assert A[np.where(A != 0)].size / float(A.size) > 0.2

    def test_png(self):
        """ Tests creation of an STL from a PNG.
        Covers the text2array function.
        """
        output_name = "OUT_.stl"
        # test ascii output
        A = imresize([[0, 1], [1, 0]], (64, 64))
        numpy2stl(A, output_name, scale=0.05, mask_val=3., ascii=True)
        assert os.path.exists(output_name)
        assert os.stat(output_name).st_size > 1500000

        # test binary output
        numpy2stl(A, output_name, scale=0.05, mask_val=3., ascii=False)
        assert os.path.exists(output_name)
        assert os.stat(output_name).st_size > 200000
        os.remove(output_name)

    def test_calc_normals(self):
        output_name = "OUT_.stl"
        A = imresize([[0, 1], [1, 0]], (64, 64))
        numpy2stl(A, output_name, scale=0.05, mask_val=3., calc_normals=True)
        assert os.path.exists(output_name)
        assert os.stat(output_name).st_size > 200000
        os.remove(output_name)

if __name__ == '__main__':
    unittest.main()
