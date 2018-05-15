![Alt text](http://i.imgur.com/CdZzhBp.png "Screenshot")

stl_tools
=======================
<!--[![Build Status](https://travis-ci.org/thearn/stl_tools.png?branch=master)](https://travis-ci.org/thearn/stl_tools)-->

Python code to generate STL geometry files from plain text, LaTeX code, and 2D numpy arrays (matrices).

This allows for rapid 3D printing of text, rendered equations, or simple digital images.
Use them for product prototyping, art, cookie cutters, ice cube trays, chocolate molds, (see [this](http://www.makerbot.com/tutorials/making-chocolate-molds/)
to learn how to make a printed object food-safe) or whatever else you can think of.

Some modification may be needed to the STL or printer settings to get certain shapes to print cleanly (i.e. thicker base,
support structures, etc).

Besides printing, these can also be merged into other 3D meshes for many other
possible uses, using programs such as [Blender](http://www.blender.org/).

Also included is a function that can convert raw LaTeX expressions to high
quality .png images, which allows for simple inclusion of LaTeX equations into
non-LaTeX document editors.

 A command-line script for converting images to STL (no text yet) is included in the installation for those who do not
want to write Python code directly.

## Requirements:
- [Python](http://python.org/) 2.7+ or 3.2+
- [Numpy](http://www.numpy.org/) 1.7 or higher (for array manipulation)
- [Scipy](http://www.scipy.org/) 0.12 or higher (for resizing and filtering functions)
- [Matplotlib](http://matplotlib.org/) 1.2.1 or higher (for rendering text and LaTeX to image data)
- [SciKitImage](http://scikit-image.org/) 0.13.1 or higher (for loading / manipulating images)

## Installation:
Build the docker container using the command:

```
  docker build -t stl_tools
```

and run the container using the command:

```
docker run -v /tmp/output:/output -it stl /bin/bash
```

** When using the container, any files placed in the `/output` folder of the container will be available in `/tmp/output` on the host.

## Quickstart Examples:

Run the example using the command `python test.py` to produce a few sample STL files from images included in `examples` directory.

## Library usage:
There are 3 principal functions (no classes) to import and use from stl_tools:

### `stl_tools.numpy2stl`
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

Each element of the array is tessellated to its neighbors to produce 2 triangular faces for
every 4 contiguous elements. The depth axis of any vertex is taken to be the value of the array corresponding to that point.

The `scale` argument scales the height of the resulting geometry. It's a similar effect to extruding or shrinking.

The `mask_val` argument allows you to set a threshold value for elements in the input array for exclusion in the STL file.
Array elements which are less than this value will not be included as vertices.
It takes a bit of trial-and-error to get these just right. Plotting the intermediate arrays
with a colorbar (to show scaling) helps in finding decent values.

The `max_width`, `max_height`, and `max_depth` values are measurements (in mm) used to scale the final output to
the largest size that can fit onto your 3D printer platform. Default values are for the MakerBot Replicator.


### `stl_tools.text2png`
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

### `stl_tools.text2array`
    text2array(text)
    Renders inputted text, and returns array representation.

    Inputs:
     text (string) -  text to render

    Returns: A (ndarray) - 2D numpy array of rendered text


`text2array()` renders inputted text using `text2png()`, but imports the resulting png as an ndarray and deletes the intermediate file.
There may be a direct way to render the matplotlib figure as an array without using an intermediate file, but I could not seem to find a simple
way in the matplotlib docs.

## Tips:

- Consider scaling down a digital image before generating an STL from its pixels.
For images of standard sizes for modern cameras, the resulting STL file size can be pretty large.

- Just like was shown in the examples, applying a simple filtering function to smooth
sharp edges results in an STL geometry that is likely to be more easily printable. Fine tuning in a
program like Photoshop or Gimp can also help prevent spikes/jagged edges in the geometry.

- To make a proper mold, scale up the edges of the source image to match the maximum pixel value of the image (or higher), to form a lip.
For example:
```python
m, n = A.shape
border_val = 1.1 * A.max()
A[0::m-1, :] = border_val # make top and bottom lip
A[:, 0::n-1] = border_val # make left and right lip
```
In practice, the border may need to be thicker than 1 pixel.

## Known bugs:

- `scipy.misc.imread` has some odd behavior for me on my Linux box (64-bit
Mint 15). When an image is read, an empty 0-dim array is returned. This is
supposedly due to a versioning issue with PIL, which I can't seem to work
around successfully. `pylab.imread` works fine, and seems consistent
across platforms.


## Todo/future features:

- Photos of actual printed models.

- I'm looking into writing a utility function to refine STL meshes by removing redundant vertices (so that wide flat spaces aren't packed with dense tessellations)

- It's possible to apply various warping functions to the resulting
meshes. So you could load an image, warp the result into a cylinder, and have a
textured column (or something like that).
