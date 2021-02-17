#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Profile time usage of cython implementation and compare to the other methods
"""

if __name__ == "__main__":
    import sys

    from cython_color2sepia import cython_color2sepia
    from numba_color2sepia import numba_color2sepia
    from numpy_color2sepia import numpy_color2sepia
    from python_color2sepia import python_color2sepia

    sys.path.insert(0, '../profiling/')
    from manual_timing_ import timer_results

    # Visual verification of implementation
    cython_color2sepia("../images/rain.jpg")

    # Profile time
    imagefile = "../images/laperm_kitten.jpg"  # shape: (1537, 2305, 3)
    numba_color2sepia(imagefile)  # call once before benchmark
    n_experiments = 5
    funcs = [python_color2sepia, numpy_color2sepia,
             numba_color2sepia, cython_color2sepia]
    args = [imagefile, imagefile, imagefile, imagefile]
    timer_results(n_experiments, "./reports/cython_report_color2sepia.txt",
                  funcs, args, order="cython_color2sepia")
