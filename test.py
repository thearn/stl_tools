import os
import skimage

from stl_tools import numpy2stl
from pylab import imread
from skimage import io
from skimage.transform import resize

A = io.imread("examples/01.png")
A = A[:, :, 2] + 1.0*A[:,:, 0]

numpy2stl(A, "madeleine.stl", scale=0.05, mask_val=5., solid=True)
