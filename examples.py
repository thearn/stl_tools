from stl_tools import numpy2stl, text2png, text2array

from scipy.misc import imread
from scipy.ndimage import gaussian_filter
from scipy.misc import lena, imresize

"""
Some quick examples
"""

A = imresize(lena(), (256,256)) # load Lena image, shrink in half
A = gaussian_filter(A, 1) # smoothing
numpy2stl(A, "examples/Lena.stl", scale=0.1)

from scipy.misc import lena, imresize
A = imresize(lena(), (256,256))
A = gaussian_filter(A, 1) #smoothing
numpy2stl(A, "examples/Lena.stl", scale=0.1)

A = imread("examples/example_data/NASA.png")
A = A[:,:,2] + 1.0*A[:,:,0] # Compose some elements from RGBA channels to give depth 
A = gaussian_filter(A, 1) # smoothing
numpy2stl(A, "examples/NASA.stl", scale=0.05, mask_val = 5.)

A = imread("examples/example_data/openmdao.png")
A =  A[:,:,0] + 1.*A[:,:,3] # Compose some elements from RGBA to give depth 
A = gaussian_filter(A, 2) # smoothing
numpy2stl(A, "examples/OpenMDAO-logo.stl", scale=0.05, mask_val = 1.)

text = ("$\oint_{\Gamma} (A\, dx + B\, dy) = \iint_{U} \left(\\frac{\partial "
        "B}{\partial x} - \\frac{\partial A}{\partial y}\\right)\ dxdy$ \n\n "
        "$\\frac{\partial \\rho}{\partial t} + \\frac{\partial}{\partial x_j}"
        "\left[ \\rho u_j \\right] = 0$")
text2png(text, "examples/Greens-Theorem_Navier-Stokes", fontsize=50) #save png 
A = imread("examples/Greens-Theorem_Navier-Stokes.png") # read from rendered png
A = A.mean(axis=2) #grayscale projection
A = gaussian_filter(A.max() - A, 1.0) 
numpy2stl(A, "examples/Greens-Theorem_Navier-Stokes.stl", scale=0.2, 
                                                         mask_val = 5.)
