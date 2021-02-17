#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from instapy.filters import grayscale_image, sepia_image

imgs = ["./images/rain.jpg", "./images/laperm_kitten.jpg"]

for img in imgs:
    gray_img = grayscale_image(img, outfile="auto", method="numba")

for img in imgs:
    sepia_img = sepia_image(img, outfile="auto", method="cython")
