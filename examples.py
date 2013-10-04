from scipy.misc import imread
from scipy.ndimage import median_filter
from stl_tools import numpy2stl, text2png, text2array

"""
Some quick examples
"""

from scipy.misc import lena
A = lena()
A = median_filter(A, size=(5, 5)) #smoothing
numpy2stl(A, "examples/Lena.stl", scale=0.25)


A = imread("examples/example_data/openmdao.png")
A =  A[:,:,0] + 1.*A[:,:,3] #Compose some elements from RGBA to give desired depth 
A = median_filter(A, size=(3,3)) #smoothing
numpy2stl(A, "examples/OpenMDAO-logo.stl", scale=0.05, mask_val = 1.)


A = imread("examples/example_data/nasa.png")
A = A[:,:,2] + 1.0*A[:,:,0] #Compose some elements from RGBA to give desired depth 
A = median_filter(A, size=(4,4)) #smoothing
numpy2stl(A, "examples/NASA.stl", scale=0.1, mask_val = 5.)


text = "Hello World!"
A = text2array(text).mean(axis=2) #grayscale projection
numpy2stl(A.max() - A, "examples/HelloWorld.stl", scale=0.6, mask_val=1)


text = "$\\frac{\partial \\rho}{\partial t} + \\frac{\partial}{\partial x_j}\left[ \\rho u_j \\right] = 0$"
text2png(text, "examples/Navier-Stokes") #save png of rendered equation (optional)
A = imread("examples/Navier-Stokes.png") #read from rendered png
A = A.mean(axis=2) #grayscale projection
A = median_filter(A.max() - A, size=(4,4)) #smoothing
numpy2stl(A, "examples/Navier-Stokes.stl", scale=0.5, mask_val = 5.)
