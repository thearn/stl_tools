from argparse import ArgumentParser

import numpy as np
from numpy2stl import numpy2stl
from pylab import imread
from scipy.ndimage import gaussian_filter


_float_args = ["scale", "mask_val", "max_width", "max_depth", "max_height"]
_bool_args = ["ascii", "calc_normals"]


def image2stl():
    """
    Provides a command-line interface to numpy2stl
    """

    parser = ArgumentParser()
    parser.add_argument("f", help='Source image filename')
    parser.add_argument("-o", default="", help='Output filename')

    parser.add_argument("-RGBA_weights", default=[""], nargs=4)
    parser.add_argument("-gaussian_filter", default="")

    float_group = parser.add_argument_group('float inputs:')
    for varname in _float_args:
        float_group.add_argument(''.join(["-", varname]), default="")

    bool_group = parser.add_argument_group('boolean inputs')
    for varname in _bool_args:
        bool_group.add_argument(''.join(["-", varname]), default="")

    args = vars(parser.parse_args())

    f_args = {f_arg: float(args[f_arg])
              for f_arg in _float_args if args[f_arg]}
    b_args = {b_arg: bool(int(args[b_arg]))
              for b_arg in _bool_args if args[b_arg]}

    kwargs = dict(f_args, **b_args)

    src = args['f']
    fn = args['o']
    if not fn:
        fn = '.'.join([src.split('.')[0], "stl"])

    A = 256. * imread(src)
    L = len(A.shape)
    w = args['RGBA_weights']
    if L > 2:
        if len(w) >= L:
            A = np.sum([float(w[i]) * A[:, :, i]
                       for i in range(A.shape[-1])], axis=0)
        else:
            A = A.mean(axis=2)

    if args['gaussian_filter']:
        A = gaussian_filter(A, float(args['gaussian_filter']))

    numpy2stl(A, fn, **kwargs)

if __name__ == "__main__":
    image2stl()
