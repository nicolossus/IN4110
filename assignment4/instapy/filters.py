#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import cv2
import numba
import numpy as np

from ._cython import _cython_color2gray, _cython_color2sepia
from ._numba import _numba_color2gray, _numba_color2sepia
from ._numpy import _numpy_color2gray, _numpy_color2sepia
from ._python import _python_color2gray, _python_color2sepia


def grayscale_image(imagefile, outfile=None, scale=None, method="numpy"):
    """
    Grayscale image filter.

    Turn a colorful image of choice into a dramatic grayscale image with method
    of choice. The new image can be saved to a specified location. The new
    image can also be up/downscaled while preserving the aspect ratio of the
    original.

    Arguments
    ---------
    imagefile : str
        Image filename (with path included) of image with shape (H, W, c) to
        transform
    outfile : str, optional, default None
        Image filename (with path included) if transformed image with shape
        (H, W) should be saved. Keyword 'auto' will save the new image in
        the same destination as the original with the transformation added to
        the original filename.
    scale : float, optional, default None
        Scale factor to resize image as fraction, e.g. 0.5 halves image
        dimensions whereas 2 doubles
    method : str, optional, default 'numpy'
        Choose implementation to use; either ["python", "numpy", "numba", "cython"]

    Returns
    -------
    grayscale_image : array, shape = (H, W)
        Transformed image as array

    Raises
    ------
    ValueError : if 'method' is not one of ['python', 'numpy', 'numba', 'cython']
    """
    allowed_methods = ["python", "numpy", "numba", "cython"]
    func_dict = {"python": _python_color2gray, "numpy": _numpy_color2gray,
                 "numba": _numba_color2gray, "cython": _cython_color2gray}
    if method in allowed_methods:
        grayscale_image = func_dict[method](imagefile, outfile, scale=scale)
    else:
        raise ValueError(
            "'method' must be one of ['python', 'numpy', 'numba', 'cython']")

    return grayscale_image


def sepia_image(imagefile, outfile=None, scale=None, sepia_amount=1, method="numpy"):
    """
    Sepia image filter.

    Turn a colorful image of choice into a nostalgic sepia image with method
    of choice. The new image can be saved to a specified location. The new
    image can also be up/downscaled while preserving the aspect ratio of the
    original.

    Arguments
    ---------
    imagefile : str
        Image filename (with path included) of image with shape (H, W, c) to
        transform
    outfile : str, optional, default None
        Image filename (with path included) if transformed image with shape
        (H, W, c) should be saved. Keyword 'auto' will save the new image in
        the same destination as the original with the transformation added to
        the original filename.
    scale : float, optional, default None
        Scale factor to resize image as fraction, e.g. 0.5 halves image
        dimensions whereas 2 doubles
    sepia_amount : float, optional, default 1.0
        0-100% amount sepia effect. 1.0 is full sepia effect, 0.0 the original image
    method : str, optional, default 'numpy'
        Choose implementation to use; either ["python", "numpy", "numba", "cython"]

    Returns
    -------
    sepia_image : array, shape = (H, W, c)
        Transformed image as array

    Raises
    ------
    ValueError : if 'method' is not one of ['python', 'numpy', 'numba', 'cython']
    """
    allowed_methods = ["python", "numpy", "numba", "cython"]
    func_dict = {"python": _python_color2sepia, "numpy": _numpy_color2sepia,
                 "numba": _numba_color2sepia, "cython": _cython_color2sepia}
    if method in allowed_methods:
        sepia_image = func_dict[method](
            imagefile, outfile, scale=scale, sepia_amount=sepia_amount)
    else:
        raise ValueError(
            "'method' must be one of ['python', 'numpy', 'numba', 'cython']")

    return sepia_image
