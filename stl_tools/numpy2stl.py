
import numpy as np
import struct

ASCII_FACET = """  facet normal  {face[0]:e}  {face[1]:e}  {face[2]:e}
    outer loop
      vertex    {face[3]:e}  {face[4]:e}  {face[5]:e}
      vertex    {face[6]:e}  {face[7]:e}  {face[8]:e}
      vertex    {face[9]:e}  {face[10]:e}  {face[11]:e}
    endloop
  endfacet"""

BINARY_HEADER ="80sI"
BINARY_FACET = "12fH"  

def _build_binary_stl(facets):
    """returns a string of binary binary data for the stl file"""

    lines = [struct.pack(BINARY_HEADER,b'Binary STL Writer',len(facets)),]
    for facet in facets: 
        facet = list(facet)
        facet.append(0) #need to pad the end with a unsigned short byte
        lines.append(struct.pack(BINARY_FACET,*facet))  
    return lines      

def _build_ascii_stl(facets): 
    """returns a list of ascii lines for the stl file """

    lines = ['solid ffd_geom',]
    for facet in facets: 
        lines.append(ASCII_FACET.format(face=facet))
    lines.append('endsolid ffd_geom')
    return lines

def writeSTL(facets, file_name, ascii=False): 
    """writes an ASCII or binary STL file"""

    f = open(file_name,'wb')
    if ascii: 
        lines = _build_ascii_stl(facets)
        f.write("\n".join(lines))
    else: 
        data = _build_binary_stl(facets)
        f.write("".join(data))

    f.close()


def numpy2stl(A, fn, scale=0.1, mask_val = -np.inf, ascii=False):
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

    Returns: (None)
    """
    A = np.rot90(A, k=3)
    m_,n_ = A.shape

    m=float(m_)
    n=float(n_)

    facets=[]
    for i in xrange(m_-1):
        for k in xrange(n_-1):
            f1 = [0,0,0]

            this_pt = [i - m/2, k - n/2, scale*A[i,k]]
            top_left = [i - m/2, k + 1 - n/2, scale*A[i,k+1]]
            bottom_left = [i + 1 - m/2, k - n/2, scale*A[i+1,k]]
            bottom_right = [i + 1 - m/2, k + 1 - n/2, scale*A[i+1,k+1]]
            
            if this_pt[-1] > mask_val and top_left[-1] > mask_val and bottom_left[-1] > mask_val:
                facets.append(f1 + this_pt + top_left + bottom_left)
            if this_pt[-1] > mask_val and bottom_right[-1] > mask_val and bottom_left[-1] > mask_val:
                facets.append(f1 + this_pt + bottom_right + bottom_left)
    facets = 0.1*np.array(facets)
    writeSTL(facets, fn, ascii=ascii)

if __name__ == "__main__":
    from scipy.misc import lena
    A = lena()
    numpy2stl(A, "lena.stl")


