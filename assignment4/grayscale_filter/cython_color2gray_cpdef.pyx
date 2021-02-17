#!/usr/bin/env python3
# cython: language_level=3

import os

import cv2
import numpy as np


cpdef cython_color2gray_cpdef(imagefile, outfile=None):
    """
    Grayscale image filter.

    Turn a colorful image of choice into a dramatic grayscale image with a
    Cython implementation. The new image can be saved to a specified
    location. By default the new image is saved in the same destination as
    the original with the transformation added to the filename.

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

    cdef int H = bgr_image.shape[0]
    cdef int W = bgr_image.shape[1]

    grayscale_image = np.empty((H, W))

    cdef int[:, :, :] bgr_view = bgr_image.astype(np.dtype("i"))
    cdef double[:, :] gray_view = grayscale_image.astype(np.dtype("d"))
    cdef int i, j

    for i in range(H):
        for j in range(W):
            gray_view[i, j] += bgr_view[i, j, 0] * 0.07 + \
                bgr_view[i, j, 1] * 0.72 + \
                bgr_view[i, j, 2] * 0.21

    grayscale_image[:, :] = gray_view
    grayscale_image = grayscale_image.astype("uint8")

    if outfile is None:
        filename, file_extension = os.path.splitext(imagefile)
        cv2.imwrite(filename + "_grayscale" + file_extension, grayscale_image)
    else:
        cv2.imwrite(outfile, grayscale_image)
