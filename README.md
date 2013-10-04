stl_tools
=======================
Python code to generate STL geometry files from plain text, LaTeX code, and 2D numpy arrays (matrices).

This allows for rapid 3D printing of text, rendered equations, or simple digital images.
Use them for product prototyping, art, cookie cutters, chocolate molds, whatever you can
think of.

Besides printing, these can also be merged into other 3D meshes for many other 
possible uses, using programs such as Blender.

Also included is a function that can convert raw LaTeX expressions to high
quality .png images, which allows for simple inclusion of LaTeX equations into 
non-LaTeX document editors.

## Requirements:
- [Python](http://python.org/) 2.7 or higher (Python 3.x not yet tested, but would probably work)
- [Numpy](http://www.numpy.org/) 1.7 or higher (for array manipulation)
- [Scipy](http://www.scipy.org/) 0.12 or higher (for image reading and filtering functions)
- [Matplotlib](http://matplotlib.org/) 1.2.1 or higher (for rendering text and LaTeX to image data)

## Usage:
Run `python setup.py build install` to install. This will check for the 
dependencies above and install the library.

There are 3 principal functions (no classes) to import and use from stl_tools:

### `numpy2stl`
    numpy2stl(A, fn, scale=0.1, mask_val = -np.inf, ascii=False, calc_normals=False)
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

     calc_normals (bool) - sets whether surface normals are calculated or not

     max_width, max_depth, max_height (floats) - maximum size of the stl
                                                object (in mm). Match this to
                                                the dimensions of a 3D printer platform 

    Returns: (None)

`numpy2stl()` is the main function of this repository. 

It takes a 2D numpy array and output filename
as input, and writes an STL file. 

Each element of the array is tesselated to its neighbors to produce 2 triangular faces for
every 4 contiguous elements. The depth axis of any vertex is taken to be the value of the array corresponding to that point.

The `scale` argument scales the height of the resulting geometry. It's a similair effect to extruding or shrinking.

The `mask_val` argument allows you to set a threshold value for elements in the input array for exclusion in the STL file.
Array elements which are less than this value will not be included as vertices.


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

from scipy.misc import lena, imresize
A = imresize(lena(), (256,256))
A = gaussian_filter(A, 1) #smoothing
numpy2stl(A, "examples/Lena.stl", scale=0.1)
```
[Click to view source image](examples/Lena.png)

[Click to view STL (view as wireframe)](examples/Lena.stl)

The next two examples convert logos to STL, using color information to achieve appropriate 3D layering

```python
A = imread("examples/example_data/openmdao.png")
A =  A[:,:,0] + 1.*A[:,:,3] #Compose some elements from RGBA to give depth 
A = gaussian_filter(A, 2) #smoothing
numpy2stl(A, "examples/OpenMDAO-logo.stl", scale=0.05, mask_val = 1.)
```
[Click to view STL (view as wireframe)](examples/OpenMDAO-logo.stl)
```python
A = imread("examples/example_data/NASA.png")
A = A[:,:,2] + 1.0*A[:,:,0] #Compose some elements from RGBA to give depth 
A = gaussian_filter(A, 1) #smoothing
numpy2stl(A, "examples/NASA.stl", scale=0.05, mask_val = 5.)
```
[Click to view source image](examples/NASA.png)

[Click to view STL (view as wireframe)](examples/NASA.stl)

Finally, this example renders a LaTeX expression into a png image, then converts this image to an STL.

```python
text = ("$\oint_{\Gamma} (A\, dx + B\, dy) = \iint_{U} \left(\\frac{\partial "
        "B}{\partial x} - \\frac{\partial A}{\partial y}\\right)\ dxdy$ \n\n "
        "$\\frac{\partial \\rho}{\partial t} + \\frac{\partial}{\partial x_j}"
        "\left[ \\rho u_j \\right] = 0$")
text2png(text, "examples/Greens-Theorem_Navier-Stokes", fontsize=50) #save png 

A = imread("examples/Greens-Theorem_Navier-Stokes.png") #read from rendered png
A = A.mean(axis=2) #grayscale projection
A = gaussian_filter(A.max() - A, 1.) #
numpy2stl(A, "examples/Greens-Theorem_Navier-Stokes.stl", scale=0.2, 
                                                         mask_val = 5.)
```
[Click to view rendered PNG](examples/Greens-Theorem_Navier-Stokes.png)

[Click to view STL (view as wireframe)](examples/Greens-Theorem_Navier-Stokes.stl)

## Tips:

- Consider scaling down a digital image before generating an STL from its pixels.
For images of standard sizes for modern cameras, the resulting STL can be quite large.

- Just like was shown in the examples, applying a simple filtering function to smooth
sharp edges results in an STL geometry that is likely to be more easily printable

## Todo/future features:

- Photos of actual printed models. 

- I'm looking into writing a utility function to refine STL meshes by removing redundant vertices (so that wide flat spaces aren't packed with dense tessellations)

- It's possible to apply various warping functions to the resulting 
meshes. So you could load an image, warp the result into a cylinder, and have a 
textured column (or something like that).

