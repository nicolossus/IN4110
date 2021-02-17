#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import cv2
import numba
import numpy as np


def numba_color2gray(imagefile, outfile=None):
    """
    Grayscale image filter.

    Turn a colorful image of choice into a dramatic grayscale image with
    automatic parallelization (and related optimizations) enabled by Numba.
    The new image can be saved to a specified location. By default the new
    image is saved in the same destination as the original with the
    transformation added to the filename.

    Arguments
    ---------
    imagefile : str
        Image filename (with path included) of image with shape (H, W, c) to
        transform
    outfile : str, optional, default None
        Image filename (with path included) if transformed image with shape
        (H, W) should be saved to a particular location
    """
    bgr_image = cv2.imread(imagefile)
    grayscale_image = _grayscale_filter(bgr_image).astype("uint8")

    if outfile is None:
        filename, file_extension = os.path.splitext(imagefile)
        cv2.imwrite(filename + "_grayscale" + file_extension, grayscale_image)
    else:
        cv2.imwrite(outfile, grayscale_image)


@numba.njit
def _grayscale_filter(bgr_image):
    """
    Grayscale kernel operation with Numba.

    Arguments
    ---------
    bgr_image : array, shape = (H, W, c)
        BGR image to transform as array

    Returns
    -------
    grayscale_image : array, shape = (H, W)
        Transformed image as array
    """
    H, W = bgr_image.shape[:2]
    grayscale_image = np.empty((H, W))
    for i in range(H):
        for j in range(W):
            grayscale_image[i, j] += bgr_image[i, j, 0] * 0.07 + \
                bgr_image[i, j, 1] * 0.72 + \
                bgr_image[i, j, 2] * 0.21

    return grayscale_image


if __name__ == "__main__":
    import sys

    from numpy_color2gray import numpy_color2gray
    from python_color2gray import python_color2gray

    sys.path.insert(0, '../profiling/')
    from manual_timing_ import timer_results

    # Visual verification of implementation
    # Also important to call function once before profiling time
    numba_color2gray("../images/rain.jpg")

    # Profile time
    imagefile = "../images/laperm_kitten.jpg"  # shape: (1537, 2305, 3)
    n_experiments = 5
    funcs = [python_color2gray, numpy_color2gray, numba_color2gray]
    args = [imagefile, imagefile, imagefile]

    timer_results(n_experiments, "./reports/numba_report_color2gray.txt",
                  funcs, args, order="numba_color2gray")
