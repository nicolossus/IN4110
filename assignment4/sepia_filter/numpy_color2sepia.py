#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import cv2
import numpy as np


def numpy_color2sepia(imagefile, outfile=None):
    """
    Sepia image filter.

    Turn a colorful image of choice into a nostalgic sepia image with the
    power of a vectorized NumPy implementation. The new image can be saved to
    a specified location. By default the new image is saved in the same
    destination as the original with the transformation added to the filename.

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
    bgr_image = np.array(bgr_image, dtype=np.float64)
    weights = np.array([[0.131, 0.534, 0.272],
                        [0.168, 0.686, 0.349],
                        [0.189, 0.769, 0.393]])  # bgr (rgb rows and cols swapped)
    sepia_image = bgr_image.dot(weights.T)
    sepia_image[np.where(sepia_image > 255)] = 255
    sepia_image = sepia_image.astype("uint8")

    if outfile is None:
        filename, file_extension = os.path.splitext(imagefile)
        cv2.imwrite(filename + "_sepia" + file_extension, sepia_image)
    else:
        cv2.imwrite(outfile, sepia_image)


if __name__ == "__main__":
    import sys

    from python_color2sepia import python_color2sepia

    sys.path.insert(0, '../profiling/')
    from manual_timing_ import timer_results

    # Visual verification of implementation
    numpy_color2sepia("../images/rain.jpg")

    # Profile time
    imagefile = "../images/laperm_kitten.jpg"  # shape: (1537, 2305, 3)
    n_experiments = 2
    funcs = [python_color2sepia, numpy_color2sepia]
    args = [imagefile, imagefile]

    timer_results(n_experiments, "./reports/numpy_report_color2sepia.txt",
                  funcs, args, order="numpy_color2sepia")
