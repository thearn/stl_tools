cimport cython
import numpy as np
cimport numpy as np
from itertools import product

try:  # python2 & python3 compatibility
    xrange
except NameError:
    xrange = range

DTYPE = np.float
ctypedef np.float_t DTYPE_t

cdef int i


@cython.boundscheck(False)
def tessellate(double[:, ::1] A,
               double mask_val,
               double min_thickness_percent,
               solid = False):
    cdef int m = A.shape[0]
    cdef int n = A.shape[1]
    cdef int i, k
    cdef int idx = 0
    cdef np.ndarray item
    cdef double[:, ::1] facets = np.zeros([4 * m * n, 12])
    cdef double[:, ::1] mask = np.zeros([m, n])

    cdef double zthickness, minval, xsize, ysize, zsize
    cdef double zmin = 1e6
    cdef double zmax = -1e6
    cdef double[:] X, Y
    cdef int facet_cut = 1

    for i in xrange(m - 1):
        for k in xrange(n - 1):
            if A[i, k] > mask_val and A[i, k + 1] > mask_val and A[i + 1, k ] > mask_val:
                facets[idx, 3] = i
                facets[idx, 4] = k + 1
                facets[idx, 5] = A[i, k + 1]

                facets[idx, 6] = i
                facets[idx, 7] = k
                facets[idx, 8] = A[i, k]

                facets[idx, 9] = i + 1
                facets[idx, 10] = k + 1
                facets[idx, 11] = A[i + 1, k + 1]

                mask[i, k + 1] = 1
                mask[i, k] = 1
                mask[i + 1, k] = 1

                idx += 1

            if A[i + 1, k + 1] > mask_val and A[i, k] > mask_val and A[i + 1, k] > mask_val:
                facets[idx, 3] = i
                facets[idx, 4] = k
                facets[idx, 5] = A[i, k]

                facets[idx, 6] = i + 1
                facets[idx, 7] = k
                facets[idx, 8] = A[i + 1, k]

                facets[idx, 9] = i + 1
                facets[idx, 10] = k + 1
                facets[idx, 11] = A[i + 1, k + 1]

                mask[i, k] = 1
                mask[i + 1, k + 1] = 1
                mask[i + 1, k] = 1

                idx += 1

    cdef double[:, ::1] edge_mask = np.sum([roll2d(mask, (i, k))
                                        for i, k in product([-1, 0, 1],
                                            repeat=2)], axis=0)

    if solid:
        facet_cut = 2
        for i in xrange(m):
            for k in xrange(n):
                if edge_mask[i,k] > 8.:
                    edge_mask[i,k] = 0.
                elif edge_mask[i,k] != 0.:
                    edge_mask[i,k] = 1.
        edge_mask[0::m - 1, :] = 1.
        edge_mask[:, 0::n - 1] = 1.

        for i in xrange(idx):
            if facets[i, 5] < zmin:
                zmin = facets[i, 5]
            elif facets[i, 5] > zmax:
                zmax = facets[i, 5]

            if facets[i, 8] < zmin:
                zmin = facets[i, 8]
            elif facets[i, 8] > zmax:
                zmax = facets[i, 8]

            if facets[i, 11] < zmin:
                zmin = facets[i, 11]
            elif facets[i, 11] > zmax:
                zmax = facets[i, 11]

        zthickness = zmax - zmin
        minval = zmin - min_thickness_percent * zthickness

        for i in xrange(idx):
            if edge_mask[ <int> facets[i, 3], <int> facets[i, 4]] != 0:
                facets[i, 5] = minval

            if edge_mask[ <int> facets[i, 6], <int> facets[i, 7]] != 0:
                facets[i, 8] = minval

            if edge_mask[ <int> facets[i, 9], <int> facets[i, 10]] != 0:
                facets[i, 11] = minval

            facets[idx+i, 3] = facets[i, 6]
            facets[idx+i, 4] = facets[i, 7]
            facets[idx+i, 5] = minval

            facets[idx+i, 6] = facets[i, 3]
            facets[idx+i, 7] = facets[i, 4]
            facets[idx+i, 8] = minval

            facets[idx+i, 9] = facets[i, 9]
            facets[idx+i, 10] = facets[i, 10]
            facets[idx+i, 11] = minval

    return facets[:facet_cut*idx]


@cython.boundscheck(False)
cdef double[:, ::1] roll2d(double[:, ::1] image, shifts):
    return np.roll(np.roll(image, shifts[0], axis=0), shifts[1], axis=1)
