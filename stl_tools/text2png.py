import pylab
import os
from scipy.misc import imread

def text2png(text, fn = None):
    """
    Renders inputted text to a png image using matplotlib.

    Inputs:
     text (string) -  text to render

    Optional input:
     fn (string)  -  filename of png to be outputted.
                     defaults to the entered text

    Returns: (None)
    """

    f = pylab.figure(frameon=False)
    ax = f.add_subplot(111)
    pylab.text(0.5, 0.5, text,
         horizontalalignment='center',
         verticalalignment='center',
         transform = ax.transAxes,
         fontsize=200)
    ax.set_axis_off()
    ax.autoscale_view(True,True,True)
    if not fn:
        fn = ''.join(e for e in text if e.isalnum())
    f.savefig(fn + '.png', bbox_inches='tight')

def text2array(text):
    """
    Renders inputted text, and returns array representation.

    Inputs:
     text (string) -  text to render

    Returns: A (ndarray) - 2D numpy array of rendered text
    """
    
    text2png(text, fn="_text")
    A = imread("_text.png")
    os.remove("_text.png")
    return A

if __name__ == "__main__":
    #LaTeX for Navier-Stokes equation
    text = "$\\frac{\partial \\rho}{\partial t} + \\frac{\partial}{\partial x_j}\left[ \\rho u_j \\right] = 0$"
    text2png(text, "NavierStokes")

