from scipy.misc import lena
from pylab import imread
from scipy.ndimage import gaussian_filter
from stl_tools import numpy2stl, text2png


"""
Some quick examples
"""

A = lena()  # load Lena image, shrink in half
A = gaussian_filter(A, 1)  # smoothing
numpy2stl(A, "examples/Lena.stl", scale=0.1, solid=False)

A = 256 * imread("examples/example_data/NASA.png")
A = A[:, :, 2] + 1.0*A[:,:, 0] # Compose RGBA channels to give depth
A = gaussian_filter(A, 1)  # smoothing
numpy2stl(A, "examples/NASA.stl", scale=0.05, mask_val=5., solid=True)

A = 256 * imread("examples/example_data/openmdao.png")
A =  A[:, :, 0] + 1.*A[:,:, 3] # Compose some elements from RGBA to give depth
A = gaussian_filter(A, 2)  # smoothing
numpy2stl(A, "examples/OpenMDAO-logo.stl",
          scale=0.05, mask_val=1., min_thickness_percent=0.005, solid=True)

text = ("$\oint_{\Gamma} (A\, dx + B\, dy) = \iint_{U} \left(\\frac{\partial "
        "B}{\partial x} - \\frac{\partial A}{\partial y}\\right)\ dxdy$ \n\n "
        "$\\frac{\partial \\rho}{\partial t} + \\frac{\partial}{\partial x_j}"
        "\left[ \\rho u_j \\right] = 0$")
# save png
text2png(text, "examples/Greens-Theorem_Navier-Stokes", fontsize=50)
# read from rendered png
A = 256 * imread("examples/Greens-Theorem_Navier-Stokes.png")
A = A.mean(axis=2)  # grayscale projection
A = gaussian_filter(A.max() - A, 1.0)
numpy2stl(A, "examples/Greens-Theorem_Navier-Stokes.stl", scale=0.15,
                                                         mask_val=5.)
