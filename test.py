from stl_tools import numpy2stl
from pylab import imread
from skimage.transform import resize

A = 256 * imread("examples/01.png")
image = resize(A, (256, 256))

numpy2stl(A, "output/madeleine.stl", scale=0.1, solid=False)
