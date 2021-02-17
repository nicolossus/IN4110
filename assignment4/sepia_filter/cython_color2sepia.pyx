#!/usr/bin/env python3
# cython: language_level=3

import os

import cv2
import numpy as np


cpdef cython_color2sepia(imagefile, outfile=None):
    """
    Sepia image filter.

    Turn a colorful image of choice into a nostalgic sepia image with a pure
    Python implementation. The new image can be saved to a specified location.
    By default the new image is saved in the same destination as the original
    with the transformation added to the filename.

    Arguments
    ---------
    imagefile : str
        Image filename (with path included) of image with shape (H, W, c) to
        transform
    outfile : str, optional, default None
        Image filename (with path included) if transformed image with shape
        (H, W, c) should be saved to a particular location
    """
    bgr_image = cv2.imread(imagefile)

    cdef int H = bgr_image.shape[0]
    cdef int W = bgr_image.shape[1]

    sepia_image = np.empty_like(bgr_image)

    cdef int[:, :, :] bgr_view = bgr_image.astype(np.dtype("i"))
    cdef double[:, :, :] sepia_view = sepia_image.astype(np.dtype("d"))
    cdef double B, G, R
    cdef int i, j

    for i in range(H):
        for j in range(W):
          B = bgr_view[i, j, 0] * 0.131 + \
              bgr_view[i, j, 1] * 0.534 + bgr_view[i, j, 2] * 0.272
          G = bgr_view[i, j, 0] * 0.168 + \
              bgr_view[i, j, 1] * 0.686 + bgr_view[i, j, 2] * 0.349
          R = bgr_view[i, j, 0] * 0.189 + \
              bgr_view[i, j, 1] * 0.769 + bgr_view[i, j, 2] * 0.393
          if B > 255:
              sepia_view[i, j, 0] = 255
          else:
              sepia_view[i, j, 0] = B
          if G > 255:
              sepia_view[i, j, 1] = 255
          else:
              sepia_view[i, j, 1] = G
          if R > 255:
              sepia_view[i, j, 2] = 255
          else:
              sepia_view[i, j, 2] = R

    sepia_image[:, :, :] = sepia_view
    sepia_image = sepia_image.astype("uint8")

    if outfile is None:
        filename, file_extension = os.path.splitext(imagefile)
        cv2.imwrite(filename + "_sepia" + file_extension, sepia_image)
    else:
        cv2.imwrite(outfile, sepia_image)
