import os
import pylab


def text2png(text, fn=None, fontsize=100):
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
               transform=ax.transAxes,
               fontsize=fontsize)
    ax.set_axis_off()
    ax.autoscale_view(True, True, True)
    if not fn:
        fn = ''.join(e for e in text if e.isalnum())
    f.savefig(fn + '.png', bbox_inches='tight')
    pylab.close()


def text2array(text, fontsize=100):
    """
    Renders inputted text, and returns array representation.

    Inputs:
     text (string) -  text to render

    Returns: A (ndarray) - 2D numpy array of rendered text
    """

    text2png(text, fn="_text", fontsize=fontsize)
    A = pylab.imread("_text.png")[:,:,:3].mean(axis=2)
    os.remove("_text.png")
    return A.max() - A

if __name__ == "__main__":
    # LaTeX for Navier-Stokes equation
    text = ("$\\frac{\partial \\rho}{\partial t} + \\frac{\partial}{\partial "
            "x_j}\left[ \\rho u_j \\right] = 0$")
    text2png(text, "NavierStokes")
