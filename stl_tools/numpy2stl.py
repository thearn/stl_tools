from itertools import product
import struct

import numpy as np


ASCII_FACET = """  facet normal  {face[0]:e}  {face[1]:e}  {face[2]:e}
    outer loop
      vertex    {face[3]:e}  {face[4]:e}  {face[5]:e}
      vertex    {face[6]:e}  {face[7]:e}  {face[8]:e}
      vertex    {face[9]:e}  {face[10]:e}  {face[11]:e}
    endloop
  endfacet"""

BINARY_HEADER = "80sI"
BINARY_FACET = "12fH"


def _build_binary_stl(facets):
    """returns a string of binary binary data for the stl file"""

    lines = [struct.pack(BINARY_HEADER, b'Binary STL Writer', len(facets)), ]
    for facet in facets:
        facet = list(facet)
        facet.append(0)  # need to pad the end with a unsigned short byte
        lines.append(struct.pack(BINARY_FACET, *facet))
    return lines


def _build_ascii_stl(facets):
    """returns a list of ascii lines for the stl file """

    lines = ['solid ffd_geom', ]
    for facet in facets:
        lines.append(ASCII_FACET.format(face=facet))
    lines.append('endsolid ffd_geom')
    return lines


def writeSTL(facets, file_name, ascii=False):
    """writes an ASCII or binary STL file"""

    f = open(file_name, 'wb')
    if ascii:
        lines = _build_ascii_stl(facets)
        f.write("\n".join(lines))
    else:
        data = _build_binary_stl(facets)
        f.write("".join(data))

    f.close()


def numpy2stl(A, fn, scale=0.1, mask_val=-np.inf, ascii=False,
              calc_normals=False,
              max_width=235.,
              max_depth=140.,
              max_height=150.):
    """
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
                                                the dimensions of a 3D printer
                                                platform

    Returns: (None)
    """
    m, n = A.shape
    if n >= m:
        A = np.rot90(A, k=3)
        m, n = n, m
    A = scale * (A - A.min())

    facets = []
    for i, k in product(xrange(m - 1), xrange(n - 1)):

        this_pt = np.array([i - m / 2., k - n / 2., A[i, k]])
        top_right = np.array([i - m / 2., k + 1 - n / 2., A[i, k + 1]])
        bottom_left = np.array([i + 1. - m / 2., k - n / 2., A[i + 1, k]])
        bottom_right = np.array(
            [i + 1. - m / 2., k + 1 - n / 2., A[i + 1, k + 1]])

        if calc_normals:
            n1 = np.cross(this_pt - top_right, bottom_left - top_right)
            n1 = n1 / np.linalg.norm(n1)

            n2 = np.cross(bottom_right - top_right, bottom_left - top_right)
            n2 = n2 / np.linalg.norm(n2)
        else:
            n1, n2 = np.zeros(3), np.zeros(3)

        if (this_pt[-1] > mask_val and top_right[-1] > mask_val and
                bottom_left[-1] > mask_val):

            facet = np.concatenate([n1, top_right, this_pt, bottom_left])
            facets.append(facet)

        if (this_pt[-1] > mask_val and bottom_right[-1] > mask_val and
                bottom_left[-1] > mask_val):

            facet = np.concatenate([n2, bottom_right, this_pt, bottom_left])
            facets.append(facet)
    facets = np.array(facets)

    xsize = facets[:, 3::3].ptp()
    if xsize > max_width:
        facets = facets * float(max_width) / xsize

    ysize = facets[:, 4::3].ptp()
    if ysize > max_depth:
        facets = facets * float(max_depth) / ysize

    zsize = facets[:, 5::3].ptp()
    if zsize > max_height:
        facets = facets * float(max_height) / zsize

    writeSTL(facets, fn, ascii=ascii)

if __name__ == "__main__":
    from scipy.misc import lena
    A = lena()
    numpy2stl(A, "lena.stl")
