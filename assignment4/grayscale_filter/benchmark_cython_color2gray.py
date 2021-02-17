#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Profile time usage of cython implementation (both with cdef and cpdef) and
compare to the other methods
"""

if __name__ == "__main__":
    import sys

    from cython_color2gray_cdef import cython_color2gray_cdef
    from cython_color2gray_cpdef import cython_color2gray_cpdef
    from numba_color2gray import numba_color2gray
    from numpy_color2gray import numpy_color2gray
    from python_color2gray import python_color2gray

    sys.path.insert(0, '../profiling/')
    from manual_timing_ import timer_results

    # Visual verification of implementation
    cython_color2gray_cdef("../images/rain.jpg")
    cython_color2gray_cpdef("../images/rain.jpg")

    # Profile time
    imagefile = "../images/laperm_kitten.jpg"  # shape: (1537, 2305, 3)
    numba_color2gray(imagefile)  # call once before benchmark
    n_experiments = 5
    funcs = [python_color2gray, numpy_color2gray, numba_color2gray,
             cython_color2gray_cdef, cython_color2gray_cpdef]
    args = [imagefile, imagefile, imagefile, imagefile, imagefile]
    timer_results(n_experiments, "./reports/cython_report_color2gray.txt",
                  funcs, args, order="cython_color2gray_cdef")
