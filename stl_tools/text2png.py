import os
import matplotlib as mpl
mpl.use('Agg', warn=False)
import matplotlib.pyplot as plt


def text2png(text, fn=None, fontsize=100, dpi=100):
    """
    Renders inputted text to a png image using matplotlib.

    Inputs:
     text (string) -  text to render

    Optional input:
     fn (string)  -  filename of png to be outputted.
                     defaults to the entered text

    Returns: (None)
    """

    f = plt.figure(frameon=False)
    ax = f.add_subplot(111)
    plt.text(0.5, 0.5, text,
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes,
             fontsize=fontsize)
    ax.set_axis_off()
    #f.set_size_inches(18.5,10.5)
    if not fn:
        fn = ''.join(e for e in text if e.isalnum())
    f.savefig(fn + '.png', bbox_inches='tight', dpi=dpi)
    plt.close()


def text2array(text, fontsize=100):
    """
    Renders inputted text, and returns array representation.

    Inputs:
     text (string) -  text to render

    Returns: A (ndarray) - 2D numpy array of rendered text
    """

    text2png(text, fn="_text", fontsize=fontsize)
    A = plt.imread("_text.png")[:, :, :3].mean(axis=2)
    os.remove("_text.png")
    return A.max() - A
