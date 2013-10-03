stl_tools
=======================
Python code to produce STL geometry files from plain text, LaTeX code, and 2D numpy arrays (matrices) 
This allows for rapid 3D printing of text, rendered equations, or simple digital images.


## Requirements:
- [Python](http://python.org/) 2.7 or higher (Python 3.x not yet tested, but would probably work)
- [Numpy](http://www.numpy.org/) 1.7 or higher (for array manipulation)
- [Scipy](http://www.scipy.org/) 0.12 or higher (for reading and filtering functions)
- [Matplotlib](http://matplotlib.org/) 1.2.1 or higher (for rendering text and LaTeX)

## Usage:

There are 3 principal functions to import from stl_tools.

### `numpy2stl`
    numpy2stl(A, fn, scale=0.1, mask_val = -np.inf, ascii=False)
    Reads a numpy array, and outputs an STL file

    Inputs:
     A (ndarray) -  an 'm' by 'n' 2D numpy array
     fn (string) -  filename to use for STL file

    Optional input:
     scale (float)  -  scales the height (surface) of the 
                       resulting STL mesh. Tune to match needs

     mask_val (float) - any element of the inputted array that is less
                        than this value will not be included in the mesh.
                        default renders all vertices (x > -inf for all float x)

     ascii (bool)  -  sets the STL format to ascii or binary (default)

    Returns: (None)

`numpy2stl()` is the main method of this repository. 

It takes a 2D numpy array and output filename
as input, and writes an STL file. 

Each element of the array is tesselated to its neighbors to produce 2 triangular faces for
every 4 contiguous elements. The depth axis of any vertex is taken to be the value of the array corresponding to that point.

The `scale` argument scales the height of the resulting geometry. It's a similair effect to extruding or shrinking.

Finally, the `mask_val` argument allows you to set a threshold value for elements in the input array for exclusion in the STL file.
Array elements which are less than this value will not be included as vertices.

NOTE: the STL file produced does not have surface normals calculated for the defined facets (they are defaulted to the vector 0,0,0).
It seems that in most applications, they are either not needed in the STL file, or are computed on the fly as needed. If someone has an application which
requires these, let me know and I can compute & include them based on an optional argument.

### `text2png`
    text2png(text, fn = None)
    Renders inputted text to a png image using matplotlib.

    Inputs:
     text (string) -  text to render

    Optional input:
     fn (string)  -  filename of png to be outputted.
                     defaults to the entered text

    Returns: (None)

`text2png()` was written as an intermediate helper function to render text to pngs, to then be imported, filtered, and meshed.
However, it may be useful in it's own right. For example, it can be used alone to render LaTeX expressions into images, to be imported into WYSIWYG document editors like MS Word or LibreOffice Writer. 

### `text2array`
    text2array(text)
    Renders inputted text, and returns array representation.

    Inputs:
     text (string) -  text to render

    Returns: A (ndarray) - 2D numpy array of rendered text
    

`text2array()` renders inputted text using `text2png()`, but imports the resulting png as an ndarray and deletes the intermediate file.
There may be a direct way to render the matplotlib figure as an array without using an intermediate file, but I could not seem to find a simple
way in the matplotlib docs.


## Examples:

Run the file `examples.py` to produce a few sample STL files.

The first example converts the commonly-used `Lena` test image to an STL file

```python
from scipy.misc import imread
from scipy.ndimage import median_filter
from stl_tools import numpy2stl, text2png, text2array

from scipy.misc import lena
A = lena()
numpy2stl(A, "examples\Lena.stl", scale=0.25)
```

The next two examples convert logos to STL, using color information to achieve appropriate 3D layering

```python
A = imread("examples\example_data\openmdao.png")
A =  A[:,:,0] + 1.*A[:,:,3] #Compose some elements from RGBA to give desired depth 
A = median_filter(A, size=(3,3)) #smoothing
numpy2stl(A, "examples\OpenMDAO-logo.stl", scale=0.05, mask_val = 5.)
```

```python
A = imread("examples\example_data\openmdao.png")
A =  A[:,:,0] + 1.*A[:,:,3] #Compose some elements from RGBA to give desired depth 
A = median_filter(A, size=(3,3)) #smoothing
numpy2stl(A, "examples\OpenMDAO-logo.stl", scale=0.05, mask_val = 5.)
```

This example converts a simple string of text to an STL file (with separate unconnected letters)

```python
text = "Hello World!"
A = text2array(text).mean(axis=2) #grayscale projection
numpy2stl(A.max() - A, "examples/HelloWorld.stl", scale=0.6, mask_val=1)
```

Finally, this example renders a LaTeX expression into a png image, then converts this image to an STL.

```python
text = "$\\frac{\partial \\rho}{\partial t} + \\frac{\partial}{\partial x_j}\left[ \\rho u_j \\right] = 0$"
text2png(text, "examples\Navier-Stokes") #save png of rendered equation (optional)
A = imread("examples\Navier-Stokes.png") #read from rendered png
A = A.mean(axis=2) #grayscale projection
A = median_filter(A.max() - A, size=(4,4)) #smoothing
numpy2stl(A, "examples\Navier-Stokes.stl", scale=0.5, mask_val = 5.)
```
