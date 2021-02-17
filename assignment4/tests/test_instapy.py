#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytest
from instapy.filters import grayscale_image, sepia_image


@pytest.mark.parametrize("implementation", ("python", "numpy", "numba", "cython"))
def test_grayscale(implementation):
    """
    Verify difference in image shape of color image (3D) and grayscale image (2D)
    Verify that a random pixel has the expected value
    """
    # generate a 3D array with pixel values randomly chosen between 0 and 255.
    np.random.seed(2020)
    low = 0
    high = 255
    N = 28
    # low (inclusive), high (exclusive)
    imarray = np.random.randint(low, high + 1, size=(N, N, 3)).astype("uint8")
    cv2.imwrite("test_image.jpg", imarray)
    imarray = cv2.imread("test_image.jpg")
    # expected random pixel value
    idx = np.random.randint(N, size=2)
    i = idx[0]
    j = idx[1]
    expected_value = imarray[i, j, :] @ np.array([0.07, 0.72, 0.21])

    gray_img = grayscale_image("test_image.jpg", method=implementation)

    # Verify dimensions
    assert imarray.shape != gray_img.shape
    assert len(gray_img.shape) == 2
    # Verify random pixel value
    assert gray_img[i, j] == int(expected_value)


@pytest.mark.parametrize("implementation", ("python", "numpy", "numba", "cython"))
def test_sepia(implementation):
    """
    Verify that a random pixel has the expected value
    """
    # generate a 3D array with pixel values randomly chosen between 0 and 255.
    np.random.seed(2020)
    low = 0
    high = 255
    N = 28
    # low (inclusive), high (exclusive)
    imarray = np.random.randint(low, high + 1, size=(N, N, 3)).astype("uint8")
    cv2.imwrite("test_image.jpg", imarray)
    imarray = cv2.imread("test_image.jpg")
    # expected random pixel value
    idx = np.random.randint(N, size=2)
    i = idx[0]
    j = idx[1]

    sepia_kernel = np.array([[0.131, 0.534, 0.272],
                             [0.168, 0.686, 0.349],
                             [0.189, 0.769, 0.393]])
    expected = (imarray[i, j, :] @ sepia_kernel.T).astype("uint8")
    expected[np.where(expected > 255)] = 255

    sepia_img = sepia_image("test_image.jpg", method=implementation)

    # Verify random pixel value
    assert np.array_equal(sepia_img[i, j, :], expected)
