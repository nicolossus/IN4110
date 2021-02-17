#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import cv2
import numpy as np


def _python_color2gray(imagefile, outfile=None, scale=None):
    """
    Grayscale image filter.

    Turn a colorful image of choice into a dramatic grayscale image with a
    pure Python implementation. The new image can be saved to a specified
    location. The new image can also be up/downscaled while preserving
    the aspect ratio of the original.

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

    Returns
    -------
    grayscale_image : array, shape = (H, W)
        Transformed image as array

    Raises
    ------
    ValueError : if 'scale' is not larger than 0
    """
    bgr_image = cv2.imread(imagefile)

    if scale is not None:
        # Up/downscale but preserve aspect ratio
        if scale > 0:
            width = int(bgr_image.shape[1] * scale)
            height = int(bgr_image.shape[0] * scale)
            dim = (width, height)
            bgr_image = cv2.resize(
                bgr_image, dim, interpolation=cv2.INTER_AREA)
        else:
            raise ValueError("'scale' must be a float larger than 0")

    # Apply grayscale kernel
    H, W = bgr_image.shape[:2]
    grayscale_image = np.zeros((H, W))
    for i in range(H):
        for j in range(W):
            grayscale_image[i, j] += bgr_image[i, j, 0] * 0.07 + \
                bgr_image[i, j, 1] * 0.72 + \
                bgr_image[i, j, 2] * 0.21

    grayscale_image = grayscale_image.astype("uint8")

    if outfile is not None:
        # Save new image
        if outfile == "auto":
            filename, file_extension = os.path.splitext(imagefile)
            cv2.imwrite(filename + "_grayscale" +
                        file_extension, grayscale_image)
        else:
            cv2.imwrite(outfile, grayscale_image)

    return grayscale_image


def _python_color2sepia(imagefile, outfile=None, scale=None, sepia_amount=1.0):
    """
    Stepless sepia image filter.

    Turn a colorful image of choice into a nostalgic sepia image with a pure
    Python implementation. The new image can be saved to a specified location.
    The new image can also be up/downscaled while preserving the aspect ratio
    of the original.

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

    Returns
    -------
    sepia_image : array, shape = (H, W, c)
        Transformed image as array

    Raises
    ------
    ValueError : if 'scale' is not larger than 0
    ValueError : if 'sepia_amount' is not a float between 0 and 1
    """
    bgr_image = cv2.imread(imagefile)

    if scale is not None:
        # Up/downscale but preserve aspect ratio
        if scale > 0:
            width = int(bgr_image.shape[1] * scale)
            height = int(bgr_image.shape[0] * scale)
            dim = (width, height)
            bgr_image = cv2.resize(
                bgr_image, dim, interpolation=cv2.INTER_AREA)
        else:
            raise ValueError("'scale' must be a float larger than 0")

    # Apply sepia kernel
    if not 0.0 <= sepia_amount <= 1.0:
        raise ValueError(
            "'sepia_amount' must be a float between 0 (no sepia effect) and 1 (full sepia effect)")

    H, W = bgr_image.shape[:2]
    sepia_image = np.zeros_like(bgr_image)
    k = 1 - sepia_amount
    for i in range(H):
        for j in range(W):
            B = bgr_image[i, j, 0] * (0.131 + 0.869 * k) + bgr_image[i, j, 1] * (
                0.534 - 0.534 * k) + bgr_image[i, j, 2] * (0.272 - 0.272 * k)
            G = bgr_image[i, j, 0] * (0.168 - 0.168 * k) + bgr_image[i, j, 1] * (
                0.686 + 0.314 * k) + bgr_image[i, j, 2] * (0.349 - 0.349 * k)
            R = bgr_image[i, j, 0] * (0.189 - 0.189 * k) + bgr_image[i, j, 1] * (
                0.769 - 0.769 * k) + bgr_image[i, j, 2] * (0.393 + 0.607 * k)

            if B > 255:
                sepia_image[i, j, 0] = 255
            elif B < 0:
                sepia_image[i, j, 0] = 0
            else:
                sepia_image[i, j, 0] = B

            if G > 255:
                sepia_image[i, j, 1] = 255
            elif G < 0:
                sepia_image[i, j, 1] = 0
            else:
                sepia_image[i, j, 1] = G

            if R > 255:
                sepia_image[i, j, 2] = 255
            elif R < 0:
                sepia_image[i, j, 2] = 0
            else:
                sepia_image[i, j, 2] = R

    sepia_image = sepia_image.astype("uint8")

    if outfile is not None:
        # Save new image
        if outfile == "auto":
            filename, file_extension = os.path.splitext(imagefile)
            cv2.imwrite(filename + "_sepia" + file_extension, sepia_image)
        else:
            cv2.imwrite(outfile, sepia_image)

    return sepia_image
