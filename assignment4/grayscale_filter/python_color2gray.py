#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import cv2
import numpy as np


def python_color2gray(imagefile, outfile=None):
    """
    Grayscale image filter.

    Turn a colorful image of choice into a dramatic grayscale image with a
    pure Python implementation. The new image can be saved to a specified
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
    H, W = bgr_image.shape[:2]
    grayscale_image = np.zeros((H, W), np.uint8)
    for i in range(H):
        for j in range(W):
            grayscale_image[i, j] += bgr_image[i, j, 0] * 0.07 + \
                bgr_image[i, j, 1] * 0.72 + \
                bgr_image[i, j, 2] * 0.21

    grayscale_image = grayscale_image.astype("uint8")

    if outfile is None:
        filename, file_extension = os.path.splitext(imagefile)
        cv2.imwrite(filename + "_grayscale" + file_extension, grayscale_image)
    else:
        cv2.imwrite(outfile, grayscale_image)


if __name__ == "__main__":
    import sys

    sys.path.insert(0, '../profiling/')
    from manual_timing_ import timer_results

    # Visual verification of implementation
    python_color2gray("../images/rain.jpg")

    # Profile time
    imagefile = "../images/laperm_kitten.jpg"  # shape: (1537, 2305, 3)
    n_experiments = 5
    funcs = [python_color2gray]
    args = [imagefile]

    timer_results(
        n_experiments, "./reports/python_report_color2gray.txt", funcs, args)
