#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import cv2
import numpy as np


def python_color2sepia(imagefile, outfile=None):
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
    H, W = bgr_image.shape[:2]
    sepia_image = np.empty_like(bgr_image)
    for i in range(H):
        for j in range(W):
            B = bgr_image[i, j, 0] * 0.131 + \
                bgr_image[i, j, 1] * 0.534 + bgr_image[i, j, 2] * 0.272
            G = bgr_image[i, j, 0] * 0.168 + \
                bgr_image[i, j, 1] * 0.686 + bgr_image[i, j, 2] * 0.349
            R = bgr_image[i, j, 0] * 0.189 + \
                bgr_image[i, j, 1] * 0.769 + bgr_image[i, j, 2] * 0.393
            if B > 255:
                sepia_image[i, j, 0] = 255
            else:
                sepia_image[i, j, 0] = B
            if G > 255:
                sepia_image[i, j, 1] = 255
            else:
                sepia_image[i, j, 1] = G
            if R > 255:
                sepia_image[i, j, 2] = 255
            else:
                sepia_image[i, j, 2] = R

    sepia_image = sepia_image.astype("uint8")

    if outfile is None:
        filename, file_extension = os.path.splitext(imagefile)
        cv2.imwrite(filename + "_sepia" + file_extension, sepia_image)
    else:
        cv2.imwrite(outfile, sepia_image)


if __name__ == "__main__":
    import sys

    sys.path.insert(0, '../profiling/')
    from manual_timing_ import timer_results

    # Visual verification of implementation
    python_color2sepia("../images/rain.jpg")

    # Profile time
    imagefile = "../images/laperm_kitten.jpg"  # shape: (1537, 2305, 3)
    n_experiments = 5
    funcs = [python_color2sepia]
    args = [imagefile]

    timer_results(
        n_experiments, "./reports/python_report_color2sepia.txt", funcs, args)
