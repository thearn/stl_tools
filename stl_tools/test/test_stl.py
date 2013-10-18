import logging
import os
import unittest
import os
import numpy as np
from stl_tools import text2array, numpy2stl, text2png

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
        Covers the numpy2stl function.
        """
        output_name = "OUT_.stl"
        # test ascii output
        A = 100 * np.random.randn(64, 64)
        numpy2stl(A, output_name, scale=0.05, mask_val=3., ascii=True)
        assert os.path.exists(output_name)
        assert os.stat(output_name).st_size > 1e5

        # test binary output
        numpy2stl(A, output_name, scale=0.05, mask_val=3.)
        assert os.path.exists(output_name)
        assert os.stat(output_name).st_size > 1e5
        os.remove(output_name)

    def test_png_force_py(self):
        """ Tests creation of an STL from a PNG.
        Covers the pure-python section of the numpy2stl function.
        """
        output_name = "OUT_.stl"
        # test ascii output
        A = 100 * np.random.randn(64, 64)
        numpy2stl(A, output_name, scale=0.05, mask_val=3., ascii=True,
                  force_python=True)
        assert os.path.exists(output_name)
        assert os.stat(output_name).st_size > 1e5

        # test binary output
        numpy2stl(A, output_name, scale=0.05, mask_val=3.,
                  force_python=True)
        assert os.path.exists(output_name)
        assert os.stat(output_name).st_size > 1e5
        os.remove(output_name)

if __name__ == '__main__':
    unittest.main()
